import sys
import boto3
import time
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from glue_etl_pipeline.utils import read_from_rds,write_to_s3
from glue_etl_pipeline.glue_config import USER_MYSQL_URL,ORDER_MYSQL_URL,PRODUCT_MYSQL_URL
from glue_etl_pipeline.logging import get_logger

# Parse job arguments
args = getResolvedOptions(sys.argv, ["JOB_NAME", "S3_TARGET_PATH"])

# Initialize Spark and Glue Context
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)
s3_output_path =args['S3_TARGET_PATH'] +args["JOB_NAME"]

# Initialize Logger
logger = get_logger("fraud detection")

def run_etl():
    start_time = time.time()
    try:
        logger.info(f"Starting ETL Job {args['JOB_NAME']}")
        user_logins_df =read_from_rds(spark,USER_MYSQL_URL,"LoginHistory")
        order_df =read_from_rds(spark,ORDER_MYSQL_URL,"Orders")

        #common tranformation 
        high_risk_customers=transform_sql()
        #high_risk_customers=transform_dataframe(order_df,user_logins_df)

        write_to_s3(high_risk_customers,s3_output_path)

        logger.info("ETL Job Completed Successfully")
    except Exception as e:
        logger.error(f"ETL Job Failed: {str(e)}")
        raise e
    finally:
        duration = time.time() - start_time
        logger.info(f"ETL Job Duration: {duration:.2f} seconds")
        job.commit()



def transform_sql():
    # Run Spark SQL Query
    query = """
    WITH suspicious_logins AS (
        SELECT
            customer_id,
            COUNT(DISTINCT ip_address) AS unique_ips,
            COUNT(*) AS total_attempts
        FROM LoginHistory
        WHERE login_date >= date_add(current_date(), -30)
        GROUP BY customer_id
        HAVING unique_ips > 3 OR total_attempts > 10
    ),
    high_risk_orders AS (
        SELECT
            customer_id,
            COUNT(order_id) AS order_count,
            SUM(total_amount) AS total_spent
        FROM Orders
        WHERE order_date >= date_add(current_date(), -30)
        GROUP BY customer_id
        HAVING total_spent > 5000 OR order_count > 5
    )
    SELECT DISTINCT s.customer_id
    FROM suspicious_logins s
    JOIN high_risk_orders h ON s.customer_id = h.customer_id
    """

    # Execute the query
    high_risk_customers = spark.sql(query)
    # Show result
    high_risk_customers.show()
    return high_risk_customers


def transform_dataframe(order_df,user_logins_df):
    # Define the date range (last 30 days)
    date_threshold = F.date_add(F.current_date(), -30)

    # Identify suspicious logins
    suspicious_logins = (
        user_logins_df.filter(F.col("login_date") >= date_threshold)
        .groupBy("customer_id")
        .agg(
            F.countDistinct("ip_address").alias("unique_ips"),
            F.count("*").alias("total_attempts")
        )
        .filter((F.col("unique_ips") > 3) | (F.col("total_attempts") > 10))
    )

    # Identify high-risk orders
    high_risk_orders = (
        order_df.filter(F.col("order_date") >= date_threshold)
        .groupBy("customer_id")
        .agg(
            F.count("order_id").alias("order_count"),
            F.sum("total_amount").alias("total_spent")
        )
        .filter((F.col("total_spent") > 5000) | (F.col("order_count") > 5))
    )

    # Join both datasets to find high-risk
    suspicious_logins.show()
    high_risk_orders.show()

    # Perform the JOIN operation
    suspicious_customers_df = suspicious_logins.join(
        high_risk_orders, 
        on="customer_id", 
        how="inner"
    ).select("customer_id").distinct()

    # Show results
    suspicious_customers_df.show()

    return suspicious_customers_df
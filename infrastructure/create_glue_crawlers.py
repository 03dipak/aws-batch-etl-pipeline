import boto3
import sys
from botocore.exceptions import ClientError

def ensure_database_exists(client, database_name):
    try:
        client.get_database(Name=database_name)
        print(f"✅ Database '{database_name}' already exists.")
    except client.exceptions.EntityNotFoundException:
        print(f"📁 Database '{database_name}' not found. Creating...")
        client.create_database(DatabaseInput={"Name": database_name})
        print(f"✅ Database '{database_name}' created successfully.")

def create_glue_crawler(crawler_name, role_arn, database_name, s3_target_path):
    client = boto3.client('glue')

    # Ensure database exists
    ensure_database_exists(client, database_name)

    # Create crawler
    try:
        response = client.create_crawler(
            Name=crawler_name,
            Role=role_arn,
            DatabaseName=database_name,
            Targets={
                'S3Targets': [
                    {'Path': s3_target_path}
                ]
            },
            TablePrefix="",  # Optional: customize if needed
            SchemaChangePolicy={
                'UpdateBehavior': 'UPDATE_IN_DATABASE',
                'DeleteBehavior': 'DEPRECATE_IN_DATABASE'
            }
        )
        print(f"✅ Crawler '{crawler_name}' created successfully.")
        return response
    except client.exceptions.AlreadyExistsException:
        print(f"⚠️ Crawler '{crawler_name}' already exists. Skipping creation.")
    except ClientError as e:
        print(f"❌ Failed to create crawler '{crawler_name}': {e}")

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python create_glue_crawlers.py <crawler_name> <role_arn> <database_name> <s3_target_path>")
        sys.exit(1)

    crawler_name = sys.argv[1]
    role_arn = sys.argv[2]
    database_name = sys.argv[3]
    s3_target_path = sys.argv[4]

    create_glue_crawler(crawler_name, role_arn, database_name, s3_target_path)

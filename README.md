# Customer 360 Analytics - AWS Glue ETL Pipeline

This project implements a batch ETL data pipeline for Customer 360 analytics using **Apache Spark on AWS Glue**. It reads data from **Amazon RDS** and **DynamoDB**, performs transformations, and stores the output in **Amazon S3**. The infrastructure and deployment are fully automated using **Boto3 scripts** and **GitHub Actions CI/CD**.

## 📁 Project Structure
<pre><code>
📦 repo-root/
┣ 📂glue_etl_pipeline                 → Modular ETL scripts for AWS Glue
┃ ┣ 📜__init__.py                     → Makes directory a Python package
┃ ┣ 📜churn_prediction.py             → Glue job for churn prediction
┃ ┣ 📜omni_channel_engagement.py      → Engagement analysis ETL
┃ ┣ 📜fraud_detection.py              → Fraud detection ETL
┃ ┣ 📜pricing_trends.py               → Price trend analysis
┃ ┣ 📜purchase_behavior.py            → Customer purchase behavior logic
┃ ┣ 📜glue_config.py                  → Constants/config for Glue jobs
┃ ┣ 📜utils.py                        → Utility functions for Glue jobs
┃ ┗ 📜logging.py                      → Centralized logging
┣ 📂glue_upload_script                → S3-uploadable Glue job scripts
┃ ┣ 📜purchase_behavior.py
┃ ┣ 📜churn_prediction.py
┃ ┣ 📜omni_channel_engagement.py
┃ ┣ 📜fraud_detection.py
┃ ┗ 📜pricing_trends.py
┣ 📂infrastructure                    → AWS resource provisioning (Boto3-based)
┃ ┣ 📜create_glue_jobs.py
┃ ┣ 📜create_glue_crawlers.py
┃ ┣ 📜create_glue_workflows.py
┃ ┣ 📜create_s3_buckets.py
┃ ┣ 📜iam_roles.py
┃ ┗ 📜deploy_infrastructure.py
┣ 📂scripts                           → Custom deployment & connection scripts
┃ ┣ 📜glue_connection.py
┃ ┗ 📜deploy_gluecustomer360_analytics_workflow.py
┣ 📂.github
┃ ┗ 📂workflows
┃   ┗ 📜deploy.yml                    → GitHub Actions CI/CD deployment workflow
┣ 📜requirements.txt                  → Python dependency definitions
┣ 📜setup.py                          → Build and package ETL as a wheel file
┗ 📜README.md                         → Project documentation and setup info
</code></pre>
## 🔧 Features
- **ETL Pipelines** for:
  - Customer Purchase Behavior
  - Churn Prediction
  - Omni-channel Engagement
  - Fraud Detection
  - Pricing Trends
- **Data Sources**: Amazon RDS (MySQL), Amazon DynamoDB
- **Data Lake Target**: Amazon S3
- **Orchestration**: AWS Glue Workflows, Triggers, and Crawlers
- **Automation**:
  - Infrastructure provisioning via Boto3
  - GitHub Actions for CI/CD deployment.
## 🧱 Architecture Overview
          +-------------------+
          |  Amazon RDS       |
          |  Amazon DynamoDB  |
          +--------+----------+
                   |
                   v
          +-------------------+
          |  AWS Glue Jobs    |  (Spark ETL)
          +--------+----------+
                   |
                   v
          +-------------------+
          |   Amazon S3       |
          +-------------------+
                   |
                   v
          +-------------------+
          |  AWS Athena       |  (Query Layer)
          +-------------------+

## 🚀 CI/CD Workflow (GitHub Actions)
The deployment pipeline automates:
Building Python wheel for Glue job logic.
Uploading job scripts and artifacts to S3.
Creating/updating Glue jobs, workflows, triggers, and crawlers.
## ⚙️ How to Set Up
1. Install Dependencies
   pip install -r requirements.txt
2. Build Python Package
   python setup.py bdist_wheel
3. Upload Job Scripts to S3
Scripts in glue_upload_script/ are synced to the designated S3 bucket folder structure.
## 🔐 Security
Uses IAM roles with least privilege principle.
CI/CD authentication via GitHub OIDC IAM role for secure access to AWS.
## 📌 Best Practices Followed
Modular and reusable ETL code (glue_etl_pipeline/)
Source and deployable code separated
Infra-as-code via Boto3
Parameterized job configurations
Centralized logging and error handling
## 📈 Future Enhancements
Add unit tests for transformations using pytest and moto
Integrate with AWS Glue Data Quality rules
Add performance metrics and CloudWatch alerts
Add versioning to deployment artifacts
Support for streaming ETL jobs (Kinesis, Kafka)
## 🧑‍💻 Author
Dipak Vaidya
Senior Software Engineer | Cloud & Data Engineering Enthusiast
<a href="https://bit.ly/2Se2UE7">LinkedIn Profile</a> | <a href="https://bit.ly/2ZaNzWp">GitHub</a>
## 📄 License
MIT License
Would you like me to help auto-fill your LinkedIn/GitHub or include a custom badge section (like build status, S3 sync success, etc.)?

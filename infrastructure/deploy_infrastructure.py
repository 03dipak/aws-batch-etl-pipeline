import subprocess

def deploy_infrastructure():
    # Step 1: Create S3 Buckets
    subprocess.run(["python", "infrastructure/create_s3_buckets.py", "your-bucket-name", "ap-south-1"])

    # Step 2: Create IAM Role for Glue
    assume_role_policy = '''{
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {
                "Service": "glue.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }]
    }'''
    policies = [
        "arn:aws:iam::aws:policy/AmazonS3FullAccess",
        "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
    ]
    subprocess.run(["python", "infrastructure/iam_roles.py", "GlueDevRole", assume_role_policy] + policies)

    # Step 3: Create Glue Jobs (example for a job)
    subprocess.run(["python", "infrastructure/create_glue_jobs.py", "churn_prediction", "arn:aws:iam::123456789012:role/GlueDevRole", "s3://your-bucket-name/code/churn_prediction.py"])

    # Step 4: Create Glue Crawlers (example for a crawler)
    subprocess.run(["python", "infrastructure/create_glue_crawlers.py", "churn_crawler", "arn:aws:iam::123456789012:role/GlueDevRole", "your-database-name", "s3://your-bucket-name/data/churn_data/"])

    # Step 5: Create Glue Workflows (example for a workflow)
    subprocess.run(["python", "infrastructure/create_glue_workflows.py", "customer360_workflow"])

if __name__ == '__main__':
    deploy_infrastructure()


    '''
    yml file code
    - name: Deploy Infrastructure (optional, if needed)
      run: |
        python infrastructure/deploy_infrastructure.py
    '''

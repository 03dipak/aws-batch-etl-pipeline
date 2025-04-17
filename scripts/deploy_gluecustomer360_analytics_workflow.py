import sys
import boto3
import time

def start_glue_job(job_name, role_arn, region, bucket_name, job_script):
    glue = boto3.client('glue', region_name=region)

    # Start the Glue job
    response = glue.start_job_run(
        JobName=job_name,
        Arguments={
            '--job-bookmark-option': 'job-bookmark-disable',
            '--s3-target-path': f"s3://{bucket_name}/analytics/{job_name}/",
            '--temp-dir': f"s3://{bucket_name}/code/temp/{job_name}/",
            '--script-location': f"s3://{bucket_name}/code/customer_analytics/{job_name}.py"
        },
        Role=role_arn
    )

    return response['JobRunId']

def monitor_job(job_name, job_run_id, region):
    glue = boto3.client('glue', region_name=region)

    # Monitor the job until it's completed
    while True:
        response = glue.get_job_run(
            JobName=job_name,
            RunId=job_run_id
        )
        status = response['JobRun']['JobRunState']

        if status in ['SUCCEEDED', 'FAILED', 'STOPPED']:
            print(f"Job {job_name} finished with status: {status}")
            return status
        print(f"Job {job_name} is still running... Status: {status}")
        time.sleep(30)

def deploy_glue_job(job_name, role_arn, region, bucket_name):
    job_run_id = start_glue_job(job_name, role_arn, region, bucket_name, job_name)
    status = monitor_job(job_name, job_run_id, region)

    if status != 'SUCCEEDED':
        print(f"Job {job_name} failed! Exiting...")
        sys.exit(1)
    print(f"Job {job_name} completed successfully.")

if __name__ == '__main__':
    job_name = sys.argv[1]
    role_arn = sys.argv[2]
    region = sys.argv[3]
    bucket_name = sys.argv[4]

    deploy_glue_job(job_name, role_arn, region, bucket_name)

"""
- name: Deploy Glue Job ${{ matrix.glue }}
        run: |
          python scripts/deploy_gluecustomer360_analytics_workflow.py \
            /$DEST_PATH/${{ matrix.glue }}-0.1.0-py3-none-any.whl \
            $ROLE_ARN $REGION $BUCKET_NAME
"""
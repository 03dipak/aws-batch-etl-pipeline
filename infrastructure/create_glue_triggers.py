import boto3
import os
import sys
import json

glue_client = boto3.client("glue", region_name=os.environ["REGION"])

def create_glue_trigger(trigger_name, workflow_name, job_name=None, prev_job_name=None, schedule_expression=None, crawler_name=None):
    trigger_params = {
        "Name": trigger_name,
        "WorkflowName": workflow_name,
        "Actions": []
    }

    if crawler_name:
        trigger_params["Actions"].append({"CrawlerName": crawler_name})
    else:
        trigger_params["Actions"].append({"JobName": job_name})

    if schedule_expression:
        trigger_params["Type"] = "SCHEDULED"
        trigger_params["Schedule"] = schedule_expression
    elif not prev_job_name:
        trigger_params["Type"] = "ON_DEMAND"
    else:
        trigger_params["Type"] = "CONDITIONAL"
        trigger_params["Predicate"] = {
            "Conditions": [{
                "LogicalOperator": "EQUALS",
                "JobName": prev_job_name,
                "State": "SUCCEEDED"
            }]
        }

    response = glue_client.create_trigger(**trigger_params)
    print(f"✅ Trigger Created: {trigger_name}")
    if prev_job_name is not None:
        glue_client.start_trigger(Name=trigger_name)
        print(f"🚀 Trigger Activated: {trigger_name}")
    return response

if __name__ == "__main__":
    BUCKET_NAME = sys.argv[3]
    REGION = sys.argv[2]
    WORKFLOW_NAME = sys.argv[5]
    CRAWLER_NAME = sys.argv[4]

    # Get job names from command line JSON string
    glue_jobs = json.loads(sys.argv[1])  # e.g., '["purchase_behavior", "churn_prediction", ...]'

    prev_job = None
    for job in glue_jobs:
        create_glue_trigger(f"trigger_{job}", WORKFLOW_NAME, job_name=job, prev_job_name=prev_job)
        prev_job = job

    create_glue_trigger(
        trigger_name=f"trigger_{CRAWLER_NAME}",
        workflow_name=WORKFLOW_NAME,
        prev_job_name=glue_jobs[-1],
        crawler_name=CRAWLER_NAME
    )

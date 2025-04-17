import boto3
import sys

def create_glue_workflow(workflow_name):
    client = boto3.client('glue')

    response = client.create_workflow(
        Name=workflow_name,
        Description='Glue Workflow for analytics jobs',
        DefaultRunProperties={}
    )
    print(f"Workflow {workflow_name} created successfully!")
    return response

if __name__ == '__main__':
    workflow_name = sys.argv[1]

    create_glue_workflow(workflow_name)

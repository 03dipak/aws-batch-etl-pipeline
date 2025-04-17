import boto3
import sys
from botocore.exceptions import ClientError

def create_glue_workflow(workflow_name):
    client = boto3.client('glue')

    try:
        # Check if the workflow already exists
        client.get_workflow(Name=workflow_name)
        print(f"✅ Workflow '{workflow_name}' already exists. Skipping creation.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityNotFoundException':
            # Workflow does not exist, so create it
            response = client.create_workflow(
                Name=workflow_name,
                Description='Glue Workflow for analytics jobs',
                DefaultRunProperties={}
            )
            print(f"🎉 Workflow '{workflow_name}' created successfully!")
            return response
        else:
            # Some other error
            raise

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("❌ Please provide the workflow name.")
        sys.exit(1)

    workflow_name = sys.argv[1]
    create_glue_workflow(workflow_name)

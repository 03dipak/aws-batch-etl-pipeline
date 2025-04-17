import boto3
import sys
from botocore.exceptions import ClientError

def create_or_update_iam_role(role_name):
    iam = boto3.client('iam')

    # Assume Role Policy Document (could be customized)
    assume_role_policy_document = '''{
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {
                "Service": "glue.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }]
    }'''

    # List of policies to attach to the role
    policies = [
        "arn:aws:iam::aws:policy/AmazonS3FullAccess",
        "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
    ]

    role_arn = ""
    try:
        # Check if the IAM role already exists
        response = iam.get_role(RoleName=role_name)
        print(f"✅ Role {role_name} already exists. Updating policies.")
        role_arn = response["Role"]["Arn"]
    except iam.exceptions.NoSuchEntityException:
        # Role does not exist, create it
        print(f"🆕 Creating IAM role {role_name}.")
        response = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=assume_role_policy_document,
            Description=f"Role for Glue Job {role_name}",
        )
        role_arn = response["Role"]["Arn"]
        print(f"✅ Role {role_name} created successfully!")

    # Attach policies to the IAM role
    for policy in policies:
        if not is_policy_attached(iam, role_name, policy):
            try:
                iam.attach_role_policy(
                    RoleName=role_name,
                    PolicyArn=policy
                )
                print(f"🔗 Policy {policy} attached to role {role_name}.")
            except ClientError as e:
                print(f"❌ Error attaching policy {policy} to role {role_name}: {str(e)}")
        else:
            print(f"✅ Policy {policy} already attached to role {role_name}, skipping.")

    # Write ARN to file
    with open("iam_role_arn.txt", "w") as f:
        f.write(role_arn)
        print(f"📄 Role ARN written to iam_role_arn.txt: {role_arn}")

    return role_arn

def is_policy_attached(iam, role_name, policy_arn):
    """Check if the given policy is already attached to the role"""
    try:
        attached_policies = iam.list_attached_role_policies(RoleName=role_name)
        return any(policy['PolicyArn'] == policy_arn for policy in attached_policies['AttachedPolicies'])
    except ClientError as e:
        print(f"❌ Error checking policy attachment for role {role_name}: {str(e)}")
        return False

if __name__ == '__main__':
    role_name = sys.argv[1]
    create_or_update_iam_role(role_name)


"""
- name: Create IAM Role
        run: python infrastructure/iam_roles.py EventDrivenRole

        or

- name: Create IAM Role for Glue Jobs
        run: |
          python infrastructure/iam_roles.py ${{ env.IAM_ROLE_NAME }}

      - name: Read IAM Role ARN
        id: read_role
        run: |
          echo "IAM_ROLE_ARN_FILE=$(cat iam_role_arn.txt)" >> "$GITHUB_ENV"

"""
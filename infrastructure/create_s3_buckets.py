import boto3
import sys

def create_s3_bucket(bucket_name, region):
    s3 = boto3.client('s3', region_name=region)

    try:
        response = s3.head_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} already exists.")
    except:
        response = s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region}
        )
        print(f"Bucket {bucket_name} created successfully in region {region}!")
    return response

if __name__ == '__main__':
    bucket_name = sys.argv[1]
    region = sys.argv[2]

    create_s3_bucket(bucket_name, region)

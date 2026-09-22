import boto3
from botocore.exceptions import ClientError

REGION = "ap-south-1"

s3 = boto3.client(
    "s3",
    region_name=REGION
)

BUCKETS = [
    "sahil-s3-task-x-050451386135",
    "sahil-s3-task-y-050451386135",
    "sahil-s3-task-z-050451386135"
]


def create_bucket(bucket_name):

    try:
        s3.head_bucket(Bucket=bucket_name)

        print(f"Bucket already exists: {bucket_name}")

    except ClientError as error:

        error_code = error.response["Error"]["Code"]

        if error_code in ["404", "NoSuchBucket"]:

            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    "LocationConstraint": REGION
                }
            )

            print(f"Created bucket: {bucket_name}")

        else:
            raise


for bucket in BUCKETS:
    create_bucket(bucket)
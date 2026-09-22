import boto3
from botocore.exceptions import ClientError

REGION = "ap-south-1"

s3 = boto3.client(
    "s3",
    region_name=REGION
)

BUCKETS = [
    "my-bucket-x-123",
    "my-bucket-y-123",
    "my-bucket-z-123"
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
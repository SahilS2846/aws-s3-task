import boto3
import json

iam = boto3.client("iam")

ACCOUNT_ID = "050451386135"
GITHUB_OWNER = "SahilS2846"
GITHUB_REPO = "aws-s3-task"
GITHUB_BRANCH = "main"

OIDC_PROVIDER = (
    f"arn:aws:iam::{ACCOUNT_ID}:oidc-provider/"
    "token.actions.githubusercontent.com"
)

def create_role(role_name, bucket_name, permissions):
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {
                "Federated": OIDC_PROVIDER
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    "token.actions.githubusercontent.com:aud":
                    "sts.amazonaws.com"
                },
                "StringLike": {
                    "token.actions.githubusercontent.com:sub":
                    f"repo:{GITHUB_OWNER}/{GITHUB_REPO}:ref:refs/heads/{GITHUB_BRANCH}"
                }
            }
        }]
    }

    iam.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(trust_policy),
        Description=f"GitHub OIDC role for {bucket_name}"
    )

    policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": permissions,
            "Resource": f"arn:aws:s3:::{bucket_name}/*"
        }]
    }

    iam.put_role_policy(
        RoleName=role_name,
        PolicyName=f"{role_name}-policy",
        PolicyDocument=json.dumps(policy)
    )

    print(f"Created role: {role_name}")


# Add role configurations here

create_role(
    "S3-Role-A",
    "my-bucket-x-123",
    [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
    ]
)

create_role(
    "S3-Role-B",
    "my-bucket-y-123",
    [
        "s3:PutObject"
    ]
)

create_role(
    "S3-Role-C",
    "my-bucket-z-123",
    [
        "s3:GetObject"
    ]
)
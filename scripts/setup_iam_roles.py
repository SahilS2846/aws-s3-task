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


def create_or_update_role(
    role_name,
    bucket_name,
    permissions,
    allow_list=False
):

    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Federated": OIDC_PROVIDER
                },
                "Action": "sts:AssumeRoleWithWebIdentity",
                "Condition": {
                    "StringEquals": {
                        "token.actions.githubusercontent.com:aud":
                            "sts.amazonaws.com",
                        "token.actions.githubusercontent.com:sub":
                            f"repo:{GITHUB_OWNER}/{GITHUB_REPO}:ref:refs/heads/{GITHUB_BRANCH}"
                    }
                }
            }
        ]
    }

    try:
        iam.get_role(RoleName=role_name)

        print(f"Role already exists: {role_name}")

        # Update trust policy
        iam.update_assume_role_policy(
            RoleName=role_name,
            PolicyDocument=json.dumps(trust_policy)
        )

        print(f"Updated trust policy: {role_name}")

    except iam.exceptions.NoSuchEntityException:

        iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description=f"GitHub OIDC role for {bucket_name}"
        )

        print(f"Created role: {role_name}")

    policy_statements = [
        {
            "Effect": "Allow",
            "Action": permissions,
            "Resource": f"arn:aws:s3:::{bucket_name}/*"
        }
    ]

    if allow_list:

        policy_statements.append(
            {
                "Effect": "Allow",
                "Action": "s3:ListBucket",
                "Resource": f"arn:aws:s3:::{bucket_name}"
            }
        )

    policy = {
        "Version": "2012-10-17",
        "Statement": policy_statements
    }

    iam.put_role_policy(
        RoleName=role_name,
        PolicyName=f"{role_name}-policy",
        PolicyDocument=json.dumps(policy)
    )

    print(f"Updated policy: {role_name}")


# Role A → Bucket X
create_or_update_role(
    "S3-Role-A",
    "sahil-s3-task-x-050451386135",
    [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
    ],
    allow_list=True
)


# Role B → Bucket Y
create_or_update_role(
    "S3-Role-B",
    "sahil-s3-task-y-050451386135",
    [
        "s3:PutObject"
    ]
)


# Role C → Bucket Z
create_or_update_role(
    "S3-Role-C",
    "sahil-s3-task-z-050451386135",
    [
        "s3:GetObject"
    ]
)
import boto3
import json

iam = boto3.client("iam")


def create_or_update_user(
    user_name,
    bucket_name,
    permissions,
    allow_list=False
):

    try:

        iam.get_user(UserName=user_name)

        print(f"User already exists: {user_name}")

    except iam.exceptions.NoSuchEntityException:

        iam.create_user(
            UserName=user_name
        )

        print(f"Created user: {user_name}")

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

    iam.put_user_policy(
        UserName=user_name,
        PolicyName=f"{user_name}-S3-Policy",
        PolicyDocument=json.dumps(policy)
    )

    print(f"Updated policy for: {user_name}")


# User A → Bucket X
create_or_update_user(
    "User-A",
    "my-bucket-x-123",
    [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
    ],
    allow_list=True
)


# User B → Upload only to Bucket Y
create_or_update_user(
    "User-B",
    "my-bucket-y-123",
    [
        "s3:PutObject"
    ]
)


# User C → Download only from Bucket Z
create_or_update_user(
    "User-C",
    "my-bucket-z-123",
    [
        "s3:GetObject"
    ]
)
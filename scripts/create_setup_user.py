import boto3
import json

iam = boto3.client("iam")

USER_NAME = "GitHub-Setup-User"

POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "iam:CreateRole",
                "iam:PutRolePolicy"
            ],
            "Resource": "*"
        }
    ]
}

# Create IAM user
iam.create_user(
    UserName=USER_NAME
)

# Attach inline policy
iam.put_user_policy(
    UserName=USER_NAME,
    PolicyName="GitHub-OIDC-Role-Setup",
    PolicyDocument=json.dumps(POLICY)
)

print(f"Created IAM user: {USER_NAME}")
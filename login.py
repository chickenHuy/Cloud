import boto3
from botocore.exceptions import ClientError

def connect_to_s3(access_key, secret_key):
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        s3.list_buckets()
        return True
    except ClientError as error:
        return False

def login_authentication(aws_access_key_id, aws_secret_access_key):
    if connect_to_s3(aws_access_key_id, aws_secret_access_key):
        return True
    else:
        return False

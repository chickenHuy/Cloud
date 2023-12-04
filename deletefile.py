import boto3
from botocore.client import Config
import time

def delete_file(aws_access_key_id, aws_secret_access_key, filename):
    try:
        s3 = boto3.resource(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            config=Config(signature_version='s3v4')
        )

        bucket_name = "awsbucket-project"
        obj = s3.Object(bucket_name, filename)
        start_time = time.time()
        obj.delete()
        end_time = time.time()
        time_delete = round(end_time - start_time, 3)
        message = "File " + filename + " deleted successfully!!! \nTime: " + str(time_delete) + "s"
        print(message)
        return message
    except Exception as e:
        return ""
    
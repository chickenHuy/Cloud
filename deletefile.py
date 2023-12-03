import boto3
from botocore.client import Config
import os

def delete_file(aws_access_key_id, aws_secret_access_key, filename):
    try:
        # Tạo đối tượng S3 từ phiên làm việc
        s3 = boto3.resource(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            config=Config(signature_version='s3v4')
        )

        bucket_name = "awsbucket-project"
        # Xóa file từ S3
        obj = s3.Object(bucket_name, filename)
        obj.delete()

        print(f"File {os.path.basename(filename)} đã được xóa khỏi {bucket_name}.")
        return True
    except Exception as e:
        print(f"Có lỗi xảy ra khi xóa file: {e}")
        return False
    
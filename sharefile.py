import boto3
from botocore.exceptions import NoCredentialsError
from botocore.client import Config

def shared_url(aws_access_key_id, aws_secret_access_key, bucket_name, filename):
    try:
        s3 = boto3.resource(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            config=Config(signature_version='s3v4')  # Sử dụng Signature Version 4
        )

        url = s3.meta.client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': filename},
            ExpiresIn=3600,
            HttpMethod='GET'
        )
        return url
    except NoCredentialsError:
        print("Thông tin đăng nhập không khả dụng")
        return None

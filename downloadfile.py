import boto3
from botocore.exceptions import NoCredentialsError
from botocore.client import Config
import os
import time

def download_file(aws_access_key_id, aws_secret_access_key, bucket_name, filename):
    try:
        s3 = boto3.resource(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            config=Config(signature_version='s3v4')
        )

        download_folder = os.path.expanduser('~/Downloads/')
        print('Start download...')
        print('Folder : ' + download_folder)
        print('File : ' + filename)
        os.makedirs(download_folder, exist_ok=True)
        local_file_path = os.path.join(download_folder, os.path.basename(filename))

        start_time = time.time()
        s3.Bucket(bucket_name).download_file(filename, local_file_path)
        end_time = time.time()
        download_time = round(end_time - start_time, 3)

        message = "File was downloaded at " + local_file_path + filename + "\nTime: " + str(download_time) + "s"
        return message

    except NoCredentialsError:
        return ""
    except Exception as e:
        return ""

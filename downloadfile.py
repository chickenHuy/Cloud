import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError
from botocore.client import Config
import os
import time

def download_file_to_download_folder(aws_access_key_id, aws_secret_access_key, bucket_name, filename, notification_placeholder):
    try:
        s3 = boto3.resource(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            config=Config(signature_version='s3v4')
        )

        download_folder = "C:/Users/Public/Downloads"
        os.makedirs(download_folder, exist_ok=True)
        local_file_path = os.path.join(download_folder, os.path.basename(filename))

        start_time = time.time()
        s3.Bucket(bucket_name).download_file(filename, local_file_path)
        end_time = time.time()
        download_time = end_time - start_time

        notification_placeholder.success(f"Tệp '{filename}' đã được tải xuống thành công! Thời gian tải xuống: {download_time:.2f} giây")
        return True
    except NoCredentialsError:
        notification_placeholder.error("Thông tin đăng nhập không khả dụng")
        return False
    except Exception as e:
        notification_placeholder.error(f"Lỗi khi tải tệp: {e}")
        return False

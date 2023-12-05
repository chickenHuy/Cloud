# import streamlit as st
import boto3
import time


def upload_file_to_s3(file, aws_access_key_id, aws_secret_access_key, folder_name):
    bucket_name = "awsbucket-project"
    
    try:
        # Tạo đối tượng S3 từ phiên làm việc
        s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

        # Định dạng tên tệp để chứa trong thư mục
        acl="private"
        file_key = f"{folder_name}{file.filename}"

        print('Start upload...')
        print('File : ' + file.filename)
        start_time = time.time()
        s3.upload_fileobj(file, bucket_name, file_key, ExtraArgs={"ACL": acl,"ContentType": file.content_type}) 
        end_time = time.time()
        upload_time = round(end_time - start_time, 3)

        message = "File was uploaded to " + folder_name + "/" + file.filename + "\nTime: " + str(upload_time) + "s"

        return message
    except Exception as e:
        return ""

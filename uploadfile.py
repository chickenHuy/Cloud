import streamlit as st
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
        file_key = f"{folder_name}{file.name}"
        start_time = time.time()
        s3.upload_fileobj(file, bucket_name, file_key)
        end_time = time.time()
        download_time = end_time - start_time
        st.success(f"Tệp '{file.name}' đã được tải lên thành công! Thời gian tải lên: {download_time:.2f} giây")
        # Tải lên tệp lên S3
        

        return True
    except Exception as e:
        st.error(f"Lỗi khi tải lên tệp: {e}")
        return False

import streamlit as st
import boto3
from botocore.exceptions import ClientError

# Hàm để kết nối đến S3
def connect_to_s3(access_key, secret_key):
    try:
        # Kết nối đến S3
        s3 = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        # Kiểm tra kết nối bằng cách liệt kê các bucket
        s3.list_buckets()
        return True
    except ClientError as error:
        st.error(f"An error occurred: {error}")
        return False

def show_login_form():
    with st.form("login_form"):
        aws_access_key_id = st.text_input("AWS Access Key ID")
        aws_secret_access_key = st.text_input("AWS Secret Access Key", type="password")
        submitted = st.form_submit_button("Đăng nhập")

        if submitted:
            if connect_to_s3(aws_access_key_id, aws_secret_access_key):
                st.success("Kết nối thành công!")
                st.session_state['aws_access_key_id'] = aws_access_key_id
                st.session_state['aws_secret_access_key'] = aws_secret_access_key
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Kết nối không thành công.")

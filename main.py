import streamlit as st
import boto3
import login
import pandas as pd
import os
from sharefile import shared_url  
from downloadfile import download_file_to_download_folder
from deletefile import delete_file
from uploadfile import upload_file_to_s3


def set_page_style():
    page_bg_img = """
    <style>
    [data-testid="stAppViewContainer"] > .main {
    background-image: url("https://img.freepik.com/free-vector/winter-blue-pink-gradient-background-vector_53876-117276.jpg");
    background-size: 250%;
    background-position: top left;
    background-repeat: no-repeat;
    background-attachment: local;
    }
    [data-testid="stHeader"] {
    background: rgba(0,0,0,0);
    }
    [data-testid="stToolbar"] {
    right: 2rem;
    }
    </style>
    """
    st.set_page_config(page_title="Đồ Án Điện Toán Đám Mây", layout="centered")
    st.markdown(page_bg_img, unsafe_allow_html=True)

def get_files_in_folder(bucket_name, selected_folder, resources):
    return [obj.key for obj in resources.Bucket(bucket_name).objects.filter(Prefix=selected_folder) if not obj.key.endswith('/')]

def main():
    set_page_style()

    if st.session_state['logged_in']:

        aws_access_key_id = st.session_state['aws_access_key_id']
        aws_secret_access_key = st.session_state['aws_secret_access_key']
        resources = boto3.resource('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        
        navigation = st.sidebar.selectbox("Navigation", ["Home", "Upload File"])

        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

        iam_client = session.client('iam')
        user_response = iam_client.get_user()
        username = user_response['User']['UserName'] + "/"

        selected_folder = username

        if navigation == "Home":
            bucket_name = "awsbucket-project"
            
            if selected_folder:
                # Lấy danh sách tệp
                st.title("📂Danh sách tệp trong thư mục📂")
                st.markdown("---")
                folder_files = get_files_in_folder(bucket_name, selected_folder, resources)
                
                shared_file_info = None
                notification_placeholder = st.empty()

                if folder_files:
                    refresh_button = st.sidebar.button("Reload danh sách file", key=f"reload_button")
                    if refresh_button:
                        get_files_in_folder(bucket_name, selected_folder, resources)

                    for i, file in enumerate(folder_files):
                        file_name = os.path.basename(file)
                        col0, col1, col2, col3, col4 = st.columns([0.5, 4.5, 1.9, 1.55, 1.65])  
                        with col0:
                            st.text(i + 1)  
                        with col1:
                            st.text(file_name)
                        with col2:
                            if st.button(f"🔽Download", key=f"download_{i}"):
                                download_file_to_download_folder(aws_access_key_id, aws_secret_access_key, bucket_name, file, notification_placeholder)

                        with col3:
                            if st.button(f"🔗Share", key=f"share_{i}"):
                                try:
                                    url = shared_url(aws_access_key_id, aws_secret_access_key, bucket_name, file)
                                    shared_file_info = (file_name, url)
                                    notification_placeholder.success(f"Share link created for {file_name}.")
                                except Exception as e:
                                    notification_placeholder.error(f"Failed to create share link for {file_name}: {e}")

                        with col4:
                            if st.button(f"❌Delete", key=f"delete_{i}"):
                                if delete_file(aws_access_key_id, aws_secret_access_key, file):
                                    notification_placeholder.success(f"{file_name} deleted successfully.")
                                else:
                                    notification_placeholder.error(f"Failed to delete {file_name}.")
                        
                if shared_file_info:
                    st.text_area(f"Copy URL for sharing {shared_file_info[0]}. It will expire in 1 hour.", shared_file_info[1], height=50)
        elif navigation == "Upload File":
            st.title("📁Trang tải lên tệp📁")
            
            # Tạo file uploader
            uploaded_file = st.file_uploader("Upload a file", type=None)
            
            # Tạo nút Upload
            upload_button = st.button("Upload")

            # Kiểm tra nếu nút Submit được nhấp và có tệp đã tải lên
            if upload_button and uploaded_file:
                # Gọi hàm tải lên
                upload_file_to_s3(uploaded_file, aws_access_key_id, aws_secret_access_key, selected_folder)

    else:
        st.warning("Vui lòng đăng nhập để tiếp tục.")


if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("Đăng nhập")
    login.show_login_form()
else:
    main()
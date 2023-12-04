import boto3
import pandas as pd
import os
from flask import *
from sharefile import shared_url  
from downloadfile import download_file
from deletefile import delete_file
from uploadfile import upload_file_to_s3


def get_files_in_folder(bucket_name, selected_folder, resources):
    return [obj.key for obj in resources.Bucket(bucket_name).objects.filter(Prefix=selected_folder) if not obj.key.endswith('/')]

def get_file():
    aws_access_key_id = session['access_key_id']
    aws_secret_access_key = session['secret_access_key']

    resources = boto3.resource('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    
    session_boto3 = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    iam_client = session_boto3.client('iam')
    user_response = iam_client.get_user()
    username = user_response['User']['UserName'] + "/"
    selected_folder = username
    session['folder_name'] = username
    bucket_name = "awsbucket-project"

    folder_files = get_files_in_folder(bucket_name, selected_folder, resources)
    json_array = []
    for i, file in enumerate(folder_files):
        file_name = os.path.basename(file)
        url = shared_url(aws_access_key_id, aws_secret_access_key, bucket_name, file)
        json_object = {
            "index": i,
            "name": file_name,
            "owner": user_response['User']['UserName'],
            "url": url,
            "file": file,
        }
        json_array.append(json_object)
    
    json_data = json.dumps(json_array)
    return json_data
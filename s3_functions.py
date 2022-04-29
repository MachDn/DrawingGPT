import boto3
import os
import re
from botocore.exceptions import ClientError


# Function to Upload Image to S3
def upload_file(file_name, bucket):
    object_name = file_name
    session = boto3.Session(region_name='eu-west-3',
		                aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
		                aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
    s3_client = session.client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name)
    return response

# Function to generate public URL from S3 to show images on the pages 
def show_image(bucket):
    session = boto3.Session(region_name='eu-west-3',
		                aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
		                aws_secret_access_key=os.environ['AWS_SECRET_KEY'])
    s3_client = session.client('s3')
    public_urls = []
    try:
        for item in s3_client.list_objects(Bucket=bucket)['Contents']:
            presigned_url = s3_client.generate_presigned_url('get_object', Params = {'Bucket': bucket, 'Key': item['Key']}, ExpiresIn = 3600)
            public_urls.append(presigned_url)
    except Exception as e:
        pass
    # print("[INFO] : The contents inside show_image = ", public_urls)
    return public_urls

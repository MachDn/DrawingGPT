import boto3
import os
import re
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from config.config import CONFIG as config


# Function to Upload Image to S3
def upload_file(file_name, bucket):
    load_dotenv()
    object_name = file_name
    # print("upload_file:{},{}".format(config['AWS']['aws_access_key_id'], config['AWS']['aws_secret_access_key']))
    
    session = boto3.Session(region_name='ap-northeast-2',
		                aws_access_key_id=config['AWS']['aws_access_key_id'],
		                aws_secret_access_key=config['AWS']['aws_secret_access_key'])
    s3_client = session.client('s3')
    print("upload_file:{},{},{}".format(file_name, bucket, object_name))
    #response = s3_client.upload_file(file_name, bucket, object_name)
    #return response

#Function to generate public URL from S3 to show images on the pages 
def show_image(bucket, new_filename):
    session = boto3.Session(region_name='ap-northeast-2',
		                aws_access_key_id=config['AWS']['aws_access_key_id'],
		                aws_secret_access_key=config['AWS']['aws_secret_access_key'])
    s3_client = session.client('s3')
    public_urls = f'https://fal-bucket.s3.ap-northeast-2.amazonaws.com/result_{new_filename}'
    try:
        for item in s3_client.list_objects(Bucket=bucket)['Contents']:
            presigned_url = s3_client.generate_presigned_url('get_object', Params = {'Bucket': bucket, 'Key': item['Key']}, ExpiresIn = 3600)
            public_urls.append(presigned_url)
    except Exception as e:
        pass
    print("[INFO] : The contents inside show_image = ", public_urls)
    return public_urls
    
    
    
    
    
    
# def show_image(file_name, bucket):
#     session = boto3.Session(region_name='ap-northeast-2',
#                             aws_access_key_id=config['AWS']['aws_access_key_id'],
#                             aws_secret_access_key=config['AWS']['aws_secret_access_key'])
#     s3_client = session.client('s3')

#     # Generate a pre-signed URL for the specified image key in the bucket
#     response = s3_client.upload_file(file_name, bucket, object_name)

#      # Generate a pre-signed URL for the uploaded image
#     presigned_url = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': object_name}, ExpiresIn=3600)


#     return presigned_url
        
        
    
    # def show_image(bucket):
    # session = boto3.Session(region_name='ap-northeast-2',
		  #              aws_access_key_id=config['AWS']['aws_access_key_id'],
		  #              aws_secret_access_key=config['AWS']['aws_secret_access_key'])
    # s3_client = session.client('s3')
    # public_urls = []
    # try:
    #     for item in s3_client.list_objects(Bucket=bucket)['Contents']:
    #         presigned_url = s3_client.generate_presigned_url('get_object', Params = {'Bucket': bucket, 'Key': item['Key']}, ExpiresIn = 3600)
    #         public_urls.append(presigned_url)
    # except Exception as e:
    #     pass
    # print("[INFO] : The contents inside show_image = ", public_urls)
    # return public_urls

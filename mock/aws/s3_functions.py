import boto3
from dotenv import load_dotenv
from os import environ
from os import remove

load_dotenv()

def upload_file(object_name: str) -> None:
    # file path for TRANSACTION source file
    PATH: str = 'mock/assets/temp/transactions.txt'

    s3 = boto3.client(service_name='s3', region_name=environ.get('AWS_REGION'),
                      aws_access_key_id=environ.get('AWS_ACCESS_KEY_ID'),
                      aws_secret_access_key=environ.get('AWS_SECRET_KEY_ID'))

    s3.upload_file(PATH, environ.get('DEV_BUCKET_NAME'), object_name)
    remove(PATH)


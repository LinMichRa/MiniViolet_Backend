import boto3
import uuid
import os
from flask import current_app

def subir_a_s3(file, folder='uploads'):
    if not file:
        return None

    s3 = boto3.client(
        's3',
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
        region_name=current_app.config['AWS_REGION']
    )

    filename = f"{folder}/{uuid.uuid4().hex}_{file.filename}"
    bucket = current_app.config['AWS_S3_BUCKET']

    s3.upload_fileobj(file, bucket, filename)

    url = f"https://{bucket}.s3.{current_app.config['AWS_REGION']}.amazonaws.com/{filename}"
    return url


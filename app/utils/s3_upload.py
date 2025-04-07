import boto3
import os
from dotenv import load_dotenv
load_dotenv()


def subir_a_s3(file):
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )

    nombre_archivo = file.filename
    bucket_name = os.getenv('AWS_BUCKET_NAME')

    try:
        s3.upload_fileobj(file, bucket_name, nombre_archivo, ExtraArgs={'ACL': 'public-read'})
        url = f"https://{bucket_name}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{nombre_archivo}"
        return url
    except Exception as e:
        print("ERROR SUBIENDO A S3:", e)
        raise

from decouple import config
import boto3
import uuid


def upload_file(file):
    r2 = boto3.client('s3',
                  endpoint_url=config("CLOUDFLARE_R2_ENDPOINT"),
                  access_key=config("CLOUDFLARE_R2_ACCESS"),
                  secret_key=config("CLOUDFLARE_R2_SECRET"))
    
    r2.upload_fileobj(file,
                        config("CLOUDFLARE_R2_BUCKET_NAME"),
                        str(uuid.uuid4()))


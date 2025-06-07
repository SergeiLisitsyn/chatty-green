from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class CustomS3Storage(S3Boto3Storage):
    def __init__(self, *args, **kwargs):
        kwargs["endpoint_url"] = f"https://s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com"
        super().__init__(*args, **kwargs)

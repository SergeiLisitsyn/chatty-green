from .base import *
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = ['chatty-green.com', 'www.chatty-green.com']

STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

DATABASES = {
    'default': dj_database_url.config(default=os.getenv("DATABASE_URL"))
}

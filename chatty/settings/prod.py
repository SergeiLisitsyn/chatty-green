from .base import *
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = [
    '.localhost',
    '127.0.0.1',
    '[::1]',
    '193.181.208.18',
    'chatty-green.com',  # 👈 обязательно
    'www.chatty-green.com',  # если есть поддомен
] 

STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

DATABASES = {
    'default': dj_database_url.config(default=os.getenv("DATABASE_URL"))
}

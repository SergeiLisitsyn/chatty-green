import os
from pathlib import Path
import dj_database_url  # Если используете Render

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')  # Обязательно через переменные окружения!

DEBUG = False
# Разрешенные хосты (добавьте домен Render/VPS после деплоя)
ALLOWED_HOSTS = [
    'chatty.onrender.com', #'your-app.onrender.com'
    'your-domain.com',
    'localhost'  # если нужно для тестов
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',


    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',

    # Наши приложения
    'users',
    'posts',
    'subscriptions',
    'widget_tweaks',
]

SITE_ID = 1

MIDDLEWARE = [
    #'whitenoise.middleware.WhiteNoiseMiddleware',  #Если используете Whitenoise (рекомендуется для Render/Railway)Добавьте после SecurityMiddleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'allauth.account.middleware.AccountMiddleware',

]
ROOT_URLCONF = 'chatty.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),  # для общей папки templates
            os.path.join(BASE_DIR, 'users/templates'),  #  это для папки с шаблонами пользователей
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {},
            'builtins': [],
        },
    },
]

WSGI_APPLICATION = 'chatty.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PG_NAME'),
        'USER': os.getenv('PG_USER'),
        'PASSWORD': os.getenv('PG_PASSWORD'),
        'HOST': os.getenv('PG_HOST'),
        'PORT': os.getenv('PG_PORT', '5432'),
        'OPTIONS': {
            'client_encoding': 'UTF8',
        },
    }
}

# Для Render: используйте их автоматическую переменную DATABASE_URL
# pip install dj-database-url

DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Authentication
AUTH_USER_MODEL = 'users.CustomUser'

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True  # включить локализацию чисел и дат
USE_TZ = True

# Static/Media
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'  # Для медиа-файлов
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'  # Для статики

# MinIO/S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL')  # Например, 'https://minio.example.com'
AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_S3_CUSTOM_DOMAIN', None)  # Если нужен кастомный CDN-URL
AWS_S3_FILE_OVERWRITE = False  # Чтобы не перезаписывать файлы с одинаковыми именами

# Для AWS S3 (если не MinIO):
AWS_S3_REGION_NAME = 'eu-north-1'
AWS_S3_SIGNATURE_VERSION = 's3v4'

# Безопасность
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') # Для Render/Railway

# HTTPS-настройки (активируйте после подключения домена)
#SECURE_HSTS_SECONDS = 31536000  # 1 год
#SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#SECURE_HSTS_PRELOAD = True
#SECURE_SSL_REDIRECT = True  # Если прокси (например, Render) поддерживает HTTPS

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}
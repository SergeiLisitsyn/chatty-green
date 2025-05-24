import os
from pathlib import Path
from dotenv import load_dotenv
from django.conf.global_settings import AUTHENTICATION_BACKENDS
from django.urls import reverse_lazy

# Определяем базовую директорию проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Загружаем переменные окружения из `.env`
load_dotenv(BASE_DIR / '.env')

# Проверка наличия `.env`
env_path = BASE_DIR / '.env'
if not env_path.exists():
    print(f"\n⚠️ Внимание: файл .env не найден по пути: {env_path}\n")

# SECURITY
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'web']

INTERNAL_IPS = [ '127.0.0.1', ]

# APPLICATIONS
INSTALLED_APPS = [
    # Сторонние пакеты
    'jazzmin',
    'django_extensions',
    'debug_toolbar',
    'widget_tweaks',

    # Django-приложения
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'social_django',
    'django.contrib.sites',

    # Аутентификация
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',



    # Твои приложения
    'users',
    'posts',
    'ads',
    'subscriptions',
]

# MIDDLEWARE
MIDDLEWARE = [
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

# URL & TEMPLATES
ROOT_URLCONF = 'chatty.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'users.context_processors.socialaccount_providers',
                # добавляем наш процессор
                ],
                'libraries': {},
                'builtins': [],

        },
    },
]

WSGI_APPLICATION = 'chatty.wsgi.application'

# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PG_NAME', ''),
        'USER': os.getenv('PG_USER', ''),
        'PASSWORD': os.getenv('PG_PASSWORD', ''),
        'HOST': os.getenv('PG_HOST', ''),
        'PORT': os.getenv('PG_PORT', ''),
        'OPTIONS': {'client_encoding': 'UTF8'},
    }
}

# PASSWORD VALIDATORS
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# LOCALIZATION
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# STATIC & MEDIA
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {
    "site_title": "Info to Chatty_green Admin",  # Заголовок административной панели
    "site_header": "CHATTY: Admin",  # Заголовок окна браузера
    "site_brand": "Info to Chatty",  # Бренд сайта
    "welcome_sign": "Welcome to CHATTY: Admin",  # Приветственное сообщение
    "copyright": "CHATTY GmbH",  # Информация о копирайте
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Support", "url": "https://google.com", "new_window": True},
    ],
    "usermenu_links": [
        {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
        {"model": "auth.user"}
    ],
    "show_sidebar": True,  # Показать боковую панель
    "navigation_expanded": True,  # Развернуть навигацию
    "hide_apps": [],  # Скрыть приложения
    "hide_models": [],  # Скрыть модели
    "default_icon_parents": "fas fa-chevron-circle-right",  # Иконка для родительских элементов
    "default_icon_children": "fas fa-circle",  # Иконка для дочерних элементов
    "related_modal_active": False,  # Включить модальные окна для связанных объектов
    "custom_css": None,  # Пользовательский CSS
    "custom_js": None,  # Пользовательский JS
    "use_google_fonts_cdn": True,  # Использовать Google Fonts CDN
    "show_ui_builder": False,  # Показать конструктор интерфейса
}


JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": "navbar-warning",
    "accent": "accent-lime",
    "navbar": "navbar-info navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-pink",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "cyborg",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": False
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)

# AUTHENTICATION
AUTH_USER_MODEL = 'users.CustomUser'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    #'social_core.backends.telegram.TelegramOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# Настройки для Google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

# Настройки для Telegram
#SOCIAL_AUTH_TELEGRAM_BOT_TOKEN = 'ВАШ_TELEGRAM_BOT_TOKEN'

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = '/'  # Страница после входа
LOGOUT_REDIRECT_URL = '/'  # Страница после выхода




SITE_ID = 1

ACCOUNT_LOGIN_METHODS = ['username']
ACCOUNT_SIGNUP_FIELDS = ['username*', 'email*', 'password1*', 'password2*']

ACCOUNT_EMAIL_VERIFICATION = "mandatory"

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_EMAIL_CONFIRMATION_HMAC = True
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = "/"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_FORMS = {'signup': 'users.forms.CustomSignupForm'}

# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', '')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)

# SOCIAL ACCOUNT
SOCIALACCOUNT_PROVIDERS = {
    'google': {
         'APP': {  # Удалите или закомментируйте этот блок!
             'client_id': os.getenv('GOOGLE_CLIENT_ID', ""),
             'secret': os.getenv('GOOGLE_CLIENT_SECRET', ""),
             'key': '',
         },
        'SCOPE': ['email', 'profile'],
        'AUTH_PARAMS': {'access_type': 'online'},
    },
    'github': {
        'SCOPE': ['user:email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    },
}

#SOCIALACCOUNT_LOGIN_ON_GET = True


# SESSION CONFIGURATION
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600
SESSION_SAVE_EVERY_REQUEST = True

# ENVIRONMENT VALIDATION
if not os.getenv('EMAIL_HOST_USER') or not os.getenv('EMAIL_HOST_PASSWORD'):
    raise ValueError("⚠️ Внимание: EMAIL_HOST_USER или EMAIL_HOST_PASSWORD не установлены! Проверьте файл .env.")







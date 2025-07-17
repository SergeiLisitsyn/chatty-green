#chatty/pipeline.py

import requests
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image
from io import BytesIO
import logging

logger = logging.getLogger(__name__)


def save_avatar(backend, user, response, *args, **kwargs):
    """
    Загружает и сохраняет аватар пользователя после Google авторизации.
    """
    if backend.name != 'google-oauth2':
        return

    avatar_url = response.get('picture')
    if not avatar_url:
        return

    try:
        # Загружаем картинку
        avatar_response = requests.get(avatar_url)
        avatar_response.raise_for_status()

        # Открываем изображение
        img = Image.open(BytesIO(avatar_response.content))
        output_size = (300, 300)
        img.thumbnail(output_size)

        buffer = BytesIO()
        img.save(buffer, format=img.format or 'JPEG')
        buffer.seek(0)

        # Сохраняем файл в S3 с уникальным именем
        filename = f'avatars/{user.username}_google_avatar.jpg'
        user.avatar.save(filename, ContentFile(buffer.read()), save=True)

    except Exception as e:
        logger.warning(f'Ошибка сохранения аватара Google для {user.username}: {e}')


def log_step(backend, user, response, *args, **kwargs):
    """
    Просто логгирует, что пользователь прошёл этап авторизации.
    """
    logger.info(f'Пользователь {user.username} успешно зарегистрирован через {backend.name}')



#users/models.py
from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
# from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
import os
from chatty import settings
from io import BytesIO

def avatar_upload_path(instance, filename):
    return f'avatars/user_{instance.user.id}/{filename}'


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.base.AUTH_USER_MODEL,  # Используем кастомную модель
        on_delete=models.CASCADE,
        related_name='profile'
    )

    def __str__(self):
        return f'Профиль пользователя {self.user.username}'


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        avatar_field = self.user.avatar
        if avatar_field and avatar_field.name:
            try:
                # Открываем аватар как поток байтов
                with default_storage.open(avatar_field.name, 'rb') as avatar_file:
                    img = Image.open(avatar_file)
                    if img.height > 300 or img.width > 300:
                        output_size = (300, 300)
                        img.thumbnail(output_size)

                        # Сохраняем уменьшенное изображение в памяти
                        buffer = BytesIO()
                        img.save(buffer, format=img.format)
                        buffer.seek(0)

                        # Перезаписываем оригинальный файл
                        avatar_field.save(avatar_field.name, ContentFile(buffer.read()), save=False)
            except Exception as e:
                # логгирование или просто пропускаем при ошибке
                pass


    """def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Уменьшаем размер аватара при сохранении
        if self.user.avatar and os.path.exists(self.user.avatar.path):
            img_path = self.user.avatar.path
            img = Image.open(img_path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(img_path)"""


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', default='https://chatty-green.s3.eu-north-1.amazonaws.com/avatars/default.png')
    bio = models.TextField(blank=True, verbose_name="О себе")
    contacts = models.CharField(max_length=255, blank=True, verbose_name="Контакты")
    # Поле для выбора отображения email; по умолчанию скрытый
    display_email = models.BooleanField(default=False, verbose_name="Показывать мой email")

    # Новые поля для бана
    is_banned = models.BooleanField(default=False, verbose_name="Забанен")
    ban_reason = models.TextField(blank=True, null=True, verbose_name="Причина бана")
    banned_until = models.DateTimeField(blank=True, null=True, verbose_name="Забанен до")


    def __str__(self):
        return self.username



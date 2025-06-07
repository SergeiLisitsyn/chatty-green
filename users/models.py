# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.files.storage import default_storage
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from chatty import settings

def avatar_upload_path(instance, filename):
    return f'avatars/user_{instance.user.id}/{filename}'

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # Используем кастомную модель
        on_delete=models.CASCADE,
        related_name='profile'
    )

    def __str__(self):
        return f'Профиль пользователя {self.user.username}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Проверяем, существует ли аватар в S3
        if self.user.avatar and default_storage.exists(self.user.avatar.name):
            # Открываем файл из S3
            with default_storage.open(self.user.avatar.name, 'rb') as f:
                img = Image.open(f)
                img.load()  # Загружаем изображение в память

            # Уменьшаем изображение, если оно слишком большое
            if img.height > 200 or img.width > 200:
                output_size = (200, 200)
                img.thumbnail(output_size)

                # Создаём новый файл с изменённым изображением
                img_io = BytesIO()
                img_format = img.format if img.format else 'JPEG'
                img.save(img_io, format=img_format)
                img_content = ContentFile(img_io.getvalue(), name=self.user.avatar.name)

                # Сохраняем изменённый аватар обратно в S3 без вызова save модели
                self.user.avatar.save(self.user.avatar.name, img_content, save=False)
                super().save(*args, **kwargs)

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    bio = models.TextField(blank=True, verbose_name="О себе")
    contacts = models.CharField(max_length=255, blank=True, verbose_name="Контакты")
    display_email = models.BooleanField(default=False, verbose_name="Показывать мой email")

    # Поля для бана
    is_banned = models.BooleanField(default=False, verbose_name="Забанен")
    ban_reason = models.TextField(blank=True, null=True, verbose_name="Причина бана")
    banned_until = models.DateTimeField(blank=True, null=True, verbose_name="Забанен до")

    def __str__(self):
        return self.username

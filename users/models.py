# Create your models here.
#users/models.py
from django.contrib.auth.models import AbstractUser, User
from django.db import models
# from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
import os
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

        # Уменьшаем размер аватара при сохранении
        if self.user.avatar and os.path.exists(self.user.avatar.path):
            img_path = self.user.avatar.path
            img = Image.open(img_path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(img_path)


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    bio = models.TextField(blank=True, verbose_name="О себе")
    contacts = models.CharField(max_length=255, blank=True, verbose_name="Контакты")

    def __str__(self):
        return self.username



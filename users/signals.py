from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import UserProfile, CustomUser

User = settings.AUTH_USER_MODEL  # Используем кастомную модель пользователя

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Создает или обновляет профиль пользователя при сохранении модели User.
    """
    if created:
        UserProfile.objects.get_or_create(user=instance)
    else:
        # Безопасное обновление без рекурсии
        if hasattr(instance, 'profile'):
            instance.profile.save()

@receiver(post_save, sender=CustomUser)
def unban_user(sender, instance, **kwargs):
    if instance.is_banned and now() >= instance.banned_until:
        instance.is_banned = False
        instance.banned_until = None  # Очистка даты бана
        instance.save()

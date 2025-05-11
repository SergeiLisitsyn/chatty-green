# subscriptions/models.py
from django.db import models
from django.conf import settings


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscribed_authors'# через это имя можно получить список авторов, на которых подписан пользователь
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followers'# через это имя можно получить список подписчиков пользователя (автора)
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Временное поле для обнаружения изменений
    #temp_field = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['subscriber', 'author'], name='unique_subscription'),
        ]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.subscriber} подписан на {self.author}"


from django.db import models


class Advertisement(models.Model):
    title = models.CharField(max_length=200)  # Заголовок рекламы
    description = models.TextField()  # Описание рекламного объявления
    image = models.ImageField(upload_to='ads_images/', null=True, blank=True)  # Картинка рекламы
    link = models.URLField()  # Ссылка на рекламируемый ресурс
    created_at = models.DateTimeField(auto_now_add=True)  # Дата публикации рекламы
    is_active = models.BooleanField(default=True)  # Активное объявление или нет

    def __str__(self):
        return self.title


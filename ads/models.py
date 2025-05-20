from django.db import models


class Advertisement(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")  # Заголовок рекламы
    description = models.TextField(verbose_name="Описание")  # Текст рекламного объявления
    image = models.ImageField(
        upload_to='ads/images/',
        null=True,
        blank=True,
        verbose_name="Изображение"
    )  # Картинка рекламы (необязательное поле)
    video = models.FileField(
        upload_to='ads/videos/',
        null=True,
        blank=True,
        verbose_name="Видеофайл"
    )  # Видео реклама (необязательное поле)
    link = models.URLField(verbose_name="Ссылка")  # Ссылка на рекламируемый ресурс
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")  # Дата добавления
    is_active = models.BooleanField(default=True, verbose_name="Активно")  # Флаг активности

    def is_video(self):
        """Определяет, является ли объявление видеороликом"""
        return self.video and not self.image

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Рекламное объявление"
        verbose_name_plural = "Рекламные объявления"
        ordering = ['-created_at']

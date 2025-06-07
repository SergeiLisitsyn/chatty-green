# posts/models.py
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from ads.models import Advertisement
from django.contrib.auth import get_user_model
from unidecode import unidecode
import boto3
from django.conf import settings

class S3Storage:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
            endpoint_url=f"https://s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com"
        )

    def upload_file(self, local_path, bucket_name, s3_path):
        """Загружает файл в S3"""
        self.client.upload_file(local_path, bucket_name, s3_path)
        print(f"Файл загружен: s3://{bucket_name}/{s3_path}")

User = get_user_model()



class Post(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    image = models.ImageField(upload_to='post_images/')
    publication_date = models.DateTimeField(auto_now_add=True)  # Дата публикации
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    updated_at = models.DateTimeField(auto_now=True)  # Дата последнего обновления
    slug = models.SlugField(unique=True, blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_posts', blank=True)
    is_archived = models.BooleanField(default=False)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.SET_NULL, null=True, blank=True)  # Рекламный блок

    def save(self, *args, **kwargs):
        if not self.slug:
            transliterated_title = unidecode(self.title)
            slug = slugify(transliterated_title)[:45]
            counter = 1
            original_slug = slug
            while Post.objects.filter(slug=slug).exists():
                suffix = f"-{counter}"
                slug = f"{original_slug[:45 - len(suffix)]}{suffix}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)  # Сначала сохраняем объект, чтобы файл появился в системе

        if self.image:  # Загружаем файл в S3 БЕЗ ACL
            s3_storage = S3Storage()
            s3_storage.client.upload_fileobj(
                self.image.file,  # Передаём объект файла, а не путь
                settings.AWS_STORAGE_BUCKET_NAME,
                f"media/post_images/{self.image.name}"
            )

        print(f"Файл загружен в S3: s3://{settings.AWS_STORAGE_BUCKET_NAME}/media/post_images/{self.image.name}")

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

    class Meta:
        ordering = ['created_at']



class Advertisement(models.Model):
    title = models.CharField(max_length=255)  # Заголовок рекламы
    description = models.TextField()  # Описание рекламного объявления
    image = models.ImageField(upload_to='ads_images/', null=True, blank=True)  # Картинка рекламы
    link = models.URLField()  # Ссылка на рекламируемый ресурс
    created_at = models.DateTimeField(auto_now_add=True)  # Дата публикации рекламы
    is_active = models.BooleanField(default=True)  # Активное объявление или нет

    def __str__(self):
        return self.title

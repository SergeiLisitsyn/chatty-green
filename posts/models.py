from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from django.contrib.auth import get_user_model

User = get_user_model()



class Post(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    publication_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_posts', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) if self.title else 'post'
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

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

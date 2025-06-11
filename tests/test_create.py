import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from unidecode import unidecode
from django.utils.text import slugify
from django.utils import timezone
import datetime
from posts.models import Post
import pytest
from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def test_user(db):
    return User.objects.create_user(username="testuser", password="testpass123")

@pytest.fixture
def authenticated_client(test_user):
    client = Client()
    client.login(username="testuser", password="testpass123")
    return client


@pytest.mark.django_db
def test_full_user_flow(client, authenticated_client, test_user):
    # Шаг 1: Логин (если используете стандартную аутентификацию)
    login_success = authenticated_client.login(username='testuser', password='testpass123')
    assert login_success is True

    # Шаг 2: Проверка начального количества постов
    initial_count = Post.objects.count()

    # Шаг 3: Создание поста
    post_data = {
        'title': 'Test Post Title',
        'text': 'This is test post content',
        # Добавьте другие обязательные поля формы
    }

    response = authenticated_client.post(
        reverse('posts:post_create'),
        data=post_data,
        follow=True  # Чтобы следовать за редиректом
    )

    # Проверки:
    print(response.content)  # Для отладки

    # 1. Проверка что пост создан
    assert Post.objects.count() == initial_count + 1

    # 2. Получаем созданный пост
    post = Post.objects.first()
    assert post is not None

    # 3. Проверка автора
    assert post.author == test_user

    # 4. Проверка данных
    assert post.title == post_data['title']
    assert post.text == post_data['text']
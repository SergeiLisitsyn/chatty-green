# tests/test_user_flow.py
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from posts.models import Post, Comment

User = get_user_model()


@pytest.fixture
def client():
    from django.test import Client
    return Client()


@pytest.fixture
def test_user(db):
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def authenticated_client(client, test_user):
    client.login(username=test_user.username, password='testpass123')
    return client


@pytest.mark.django_db
def test_full_user_flow(client, authenticated_client, test_user):
    # Шаг 1: Регистрация пользователя (пример для django-allauth)
    registration_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password1': 'testpass123',
        'password2': 'testpass123',
    }
    response = client.post(reverse('login'), registration_data)
    assert response.status_code == 200  # Проверка редиректа после регистрации

    # Шаг 2: Создание поста
    post_data = {
        'title': 'Test Post Title',
        'text': 'This is test post content'
    }
    response = authenticated_client.post(reverse('posts:post_create'), post_data)
    assert response.status_code == 302

    # Проверка создания поста
    post = Post.objects.first()
    assert post is not None
    assert post.title == 'Test Post Title'
    assert post.author == test_user

    # Шаг 3: Добавление комментария
    comment_data = {'text': 'Great post!'}
    response = authenticated_client.post(
        reverse('posts:post_detail', kwargs={'slug': post.slug}),
        comment_data
    )
    assert response.status_code == 302

    # Проверка комментария
    comment = Comment.objects.first()
    assert comment is not None
    assert comment.text == 'Great post!'
    assert comment.author == test_user
    assert comment.post == post

    # Шаг 4: Проверка отображения данных
    response = authenticated_client.get(reverse('posts:post_detail', kwargs={'slug': post.slug}))
    content = response.content.decode()

    # Проверка содержимого страницы
    assert post.title in content
    assert post.text in content
    assert 'Great post!' in content
    assert test_user.username in content

    # Проверка контекста
    assert response.context['post'] == post
    assert comment in response.context['comments']
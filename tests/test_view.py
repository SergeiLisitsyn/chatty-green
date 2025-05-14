from django.test import TestCase

# Create your tests here.
# tests/test_views.py
import pytest
from django.urls import reverse
from posts.models import Post


@pytest.mark.django_db
class TestPostCreateView:
    # URL для вьюхи
    url = reverse("posts:post_create")

    def test_unauthorized_access_redirected_to_login(self, client):
        """Неавторизованный пользователь перенаправляется на страницу входа"""
        response = client.get(self.url)
        login_url = reverse("login") + f"?next={self.url}"
        assert response.status_code == 302
        assert response.url == login_url

    def test_authorized_user_can_access_page(self, admin_client):
        """Авторизованный пользователь видит форму создания поста"""
        response = admin_client.get(self.url)
        assert response.status_code == 200
        assert "form" in response.context
        assert "post_form.html" in [t.name for t in response.templates]

    def test_valid_form_creates_post_with_author(self, admin_user, admin_client):
        """Валидная форма создает пост с автором и делает редирект"""
        data = {
            "title": "Test Post",
            "content": "Sample content",
            # Другие обязательные поля формы
        }

        response = admin_client.post(self.url, data)

        # Проверка редиректа
        assert response.status_code == 302
        assert response.url == reverse("posts:post_list")

        # Проверка создания поста
        post = Post.objects.first()
        assert post.title == data["title"]
        assert post.author == admin_user  # Важная проверка привязки автора
        assert post.content == data["content"]

    def test_invalid_form_returns_errors(self, admin_client):
        """Невалидная форма показывает ошибки"""
        response = admin_client.post(self.url, {})
        assert response.status_code == 200
        assert "form" in response.context
        assert "Это поле обязательно." in response.content.decode()

    def test_success_url_after_creation(self, admin_client):
        """Проверка корректного success_url"""
        data = {"title": "Dummy", "content": "Content"}
        response = admin_client.post(self.url, data)
        assert response.url == reverse("posts:post_list")
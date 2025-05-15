import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.test import Client
from posts.models import Post

User = get_user_model()

@pytest.fixture
def user():
    """Создает обычного пользователя"""
    return User.objects.create_user(
        username="testuser",
        password="testpass123",
        # Добавьте обязательные поля вашей CustomUser
        email="test@example.com"
    )

@pytest.fixture
def user_client(user):
    """Клиент с авторизованным пользователем"""
    client = Client()
    client.login(username=user.username, password="testpass123")
    return client

@pytest.fixture
def another_user():
    """Другой пользователь"""
    return User.objects.create_user(
        username="another_user",
        password="testpass456",
        email="another@example.com"
    )

@pytest.mark.django_db
class TestPostUpdateView:
    @pytest.fixture
    def post(self, admin_user):
        # Создаем тестовый пост от имени администратора
        return Post.objects.create(
            title="Original Title",
            text="Original Content",
            author=admin_user,
            slug="original-title"
        )

    def get_url(self, post):
        return reverse("posts:post_update", kwargs={"slug": post.slug})

    def test_unauthorized_access_redirected_to_login(self, client, post):
        """Неавторизованный пользователь перенаправляется на логин"""
        url = self.get_url(post)
        response = client.get(url)
        expected_login_url = f"/accounts/login/?next={url}"
        assert response.status_code == 302
        assert response.url == expected_login_url


    def test_authorized_but_not_author_gets_403(self, user_client, post):
        """Авторизованный НЕ-автор получает 403"""
        url = self.get_url(post)
        response = user_client.get(url)
        assert response.status_code == 403

    def test_author_can_access_edit_page(self, admin_client, post):
        """Автор поста видит страницу редактирования"""
        url = self.get_url(post)
        response = admin_client.get(url)

        assert response.status_code == 200
        assert "posts/post_form.html" in [t.name for t in response.templates]
        assert "form" in response.context

    def test_valid_form_updates_post(self, admin_client, post):
        """Валидная форма обновляет пост и редиректит"""
        url = self.get_url(post)
        data = {
            "title": "Updated Title",
            "text": "Updated Content",
            # Другие обязательные поля формы
        }

        response = admin_client.post(url, data)

        # Проверка редиректа
        assert response.status_code == 302
        assert response.url == reverse("posts:post_detail", kwargs={"slug": post.slug})

        # Обновляем объект из БД
        post.refresh_from_db()
        assert post.title == data["title"]
        assert post.text == data["text"]
        # Проверяем что slug не изменился (если slug генерируется из title)
        assert post.slug == "original-title"

    def test_invalid_form_shows_errors(self, admin_client, post):
        """Невалидная форма показывает ошибки"""
        url = self.get_url(post)
        response = admin_client.post(url, {"title": "", "text": "Content"})

        # Проверка статуса и контекста
        assert response.status_code == 200
        assert "form" in response.context

        # Проверка ошибок в объекте формы
        form = response.context["form"]
        assert "title" in form.errors  # Ошибка должна быть в поле title
        assert 'Обязательное поле.' in form.errors["title"][0]  # Проверка текста

        # Проверка отображения ошибки в HTML
        #content = response.content.decode("utf-8")
        #assert "Это поле обязательно." in content

    def test_cannot_change_author(self, admin_client, post, another_user):
        """Попытка изменить автора должна игнорироваться"""
        url = self.get_url(post)
        original_author = post.author

        data = {
            "title": "Try Change Author",
            "text": "Content",
            "author": another_user.id  # Пытаемся изменить автора
        }

        response = admin_client.post(url, data)
        post.refresh_from_db()

        assert post.author == original_author  # Автор остался прежним
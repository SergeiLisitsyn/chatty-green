from django.test import TestCase

# Create your tests here.
# tests/test_views.py
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from unidecode import unidecode
from django.utils.text import slugify
from django.utils import timezone
import datetime
from posts.models import Post

User = get_user_model()

@pytest.mark.django_db
class TestPostCreateView:
    # URL для вьюхи
    url = reverse("posts:post_create")

    def test_unauthorized_access_redirected_to_login(self, client):
        """Неавторизованный пользователь перенаправляется на страницу входа"""
        response = client.get(self.url)
        expected_login_url = "/accounts/login/?next=/posts/create/"
        assert response.status_code == 302
        assert response.url == expected_login_url

    def test_authorized_user_can_access_page(self, admin_client):
        """Авторизованный пользователь видит форму создания поста"""
        response = admin_client.get(self.url)
        assert response.status_code == 200
        assert "posts/post_form.html" in [t.name for t in response.templates]
        assert "form" in response.context
        #assert "post_form.html" in [t.name for t in response.templates]

    def test_valid_form_creates_post_with_author(self, admin_user, admin_client):
        """Валидная форма создает пост с автором и делает редирект"""
        data = {
            "title": "Test Post",
            "text": "Sample content",
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
        assert post.text == data["text"]

    def test_invalid_form_returns_errors(self, admin_client):
        """Невалидная форма показывает ошибки"""
        response = admin_client.post(self.url, {})
        assert response.status_code == 200
        assert "form" in response.context
        assert 'Обязательное поле.' in response.content.decode()

    def test_success_url_after_creation(self, admin_client):
        """Проверка корректного success_url"""
        data = {"title": "Dummy", "text": "TestText"}
        response = admin_client.post(self.url, data)
        assert response.url == reverse("posts:post_list")

    def test_title_length_validation(self, admin_client):
        """Проверка валидации длины заголовка"""
        # Невалидные данные: title короче допустимого (например, min_length=5)
        invalid_data = {"title": "AAAA", "text": "TestText"}
        response = admin_client.post(self.url, data=invalid_data)

        # Проверяем, что нет редиректа (статус 200)
        assert response.status_code == 200, "Форма должна вернуть ошибку, а не редирект"

        # Проверяем наличие ошибки в форме
        form = response.context.get("form")
        assert form is not None, "Форма не найдена в контексте ответа"
        assert "title" in form.errors, "Ожидалась ошибка валидации поля title"

        # Проверяем текст ошибки (опционально)
        expected_error = "Заголовок должен содержать минимум 5 символов."
        assert expected_error in form.errors["title"], "Некорректное сообщение об ошибке"


    def test_csrf_protection(self, client):
        """Проверка наличия CSRF токена в форме"""

        admin_user = User.objects.create_superuser(
            username="admin",
            password="password",
            email="admin@example.com"
        )
        client.force_login(admin_user)
        response = client.get(self.url)
        assert 'csrfmiddlewaretoken' in response.content.decode()

    def test_slug_auto_generation(self, admin_client):
        """Тест авто генерации slug при создании поста"""
        data = {"title": "Test Post Title", "text": "TestText"}
        admin_client.post(self.url, data)
        post = Post.objects.first()
        assert post.slug == 'test-post-title'

    def test_cyrillic_slug_conversion(self, admin_client):
        """Тест конвертации кириллических символов в slug"""
        data = {"title": "Тестовый Заголовок", "text": "TestText"}
        admin_client.post(self.url, data)
        post = Post.objects.first()
        expected_slug = slugify(unidecode(data['title']))
        assert post.slug == expected_slug.lower()

    def test_slug_max_length(self, admin_client):
        """Тест обрезки slug до максимальной длины"""
        data = {"title": 'a' * 100, "text": "TestText"}
        admin_client.post(self.url, data)
        post = Post.objects.first()
        assert len(post.slug) <= 45
        assert post.slug == 'a' * 45

    def test_created_at_auto_set(self, admin_client):
        """Тест автоматической установки даты создания"""
        # Создаем пост и сразу получаем текущее время
        data = {"title": 'Test Title', "text": "TestText"}
        before_creation = timezone.now()
        admin_client.post(self.url, data)
        post = Post.objects.first()
        after_creation = timezone.now()

        # Проверяем что дата установлена
        assert post.created_at is not None

        # Проверяем что дата находится в ожидаемом диапазоне
        assert before_creation <= post.created_at <= after_creation

        # Дополнительная проверка с учетом микросекунд (если важно)
        time_delta = after_creation - post.created_at
        assert time_delta >= datetime.timedelta(0)

    def test_created_at_precision(self, admin_client):
        """Тест точности установки времени создания"""
        data = {"title": 'Test Title', "text": "TestText"}
        admin_client.post(self.url, data)
        current_time = timezone.now()
        post = Post.objects.first()
        # Конвертируем datetime в timestamp для сравнения
        created_ts = post.created_at.timestamp()
        current_ts = current_time.timestamp()

        # Допустимая погрешность 1 секунда
        assert created_ts == pytest.approx(current_ts, abs=1)


    def test_slug_uniqueness(self, admin_client):
        """Тест уникальности slug"""
        data = {"title": 'Test Title', "text": "TestText"}

        admin_client.post(self.url, data)
        admin_client.post(self.url, data)
        posts = Post.objects.all()
        post1, post2 = posts[0], posts[1]
        assert post1.slug != post2.slug
        assert post2.slug.startswith('test-title-')

    def test_slug_increment_suffix(self, admin_client):
        """Тест корректного добавления суффиксов при дубликатах"""
        # Создаем несколько постов с одинаковым заголовком
        data = {"title": 'Test Title', "text": "TestText"}
        slugs = []
        for i in range(5):
            admin_client.post(self.url, data)
        posts = Post.objects.all()
        for post in posts:
            slugs.append(post.slug)

        # Проверяем уникальность всех slug
        assert len(set(slugs)) == 5

        # Проверяем паттерн slug
        assert slugs[0] == 'test-title'
        assert slugs[1] == 'test-title-1'
        assert slugs[2] == 'test-title-2'
        assert slugs[3] == 'test-title-3'
        assert slugs[4] == 'test-title-4'


from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Post  # Замените myapp на имя вашего приложения

User = get_user_model()


#@pytest.mark.django_db
def test_unauthorized_user_cannot_access_post_update(client, create_post):
    # Создаем пост и получаем его slug
    post = create_post(slug="test-post")

    # Формируем URL для обновления поста
    url = reverse("post_update", kwargs={"slug": post.slug})

    # Отправляем GET-запрос неавторизованным клиентом
    response = client.get(url)

    # Проверяем статус ответа (редирект)
    assert response.status_code == 302

    # Проверяем, что редирект ведет на страницу входа
    login_url = reverse("login")  # Замените "login" на имя вашего URL для входа
    assert response.url.startswith(login_url)

    # Проверяем наличие параметра next в URL редиректа
    assert f"next={url}" in response.url


class PostAPITests(TestCase):
    def setUp(self):
        # Создаем тестовых пользователей
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass456'
        )

        # Создаем тестовый пост
        self.post = Post.objects.create(
            title='Original Title',
            text='Original Content',
            author=self.user
        )

    # Тест 1: Успешное создание поста авторизованным пользователем
    def test_authenticated_user_can_create_post(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('post_create')
        response = self.client.post(url, {
            'title': 'New Post',
            'text': 'Test Content'
        })
        print(response)
        self.assertEqual(response.status_code, 302)  # 201 Created для API
        self.assertEqual(Post.objects.count(), 2)  # Проверяем создание объекта

    # Тест 2: Неавторизованный пользователь не может создать пост

    def test_unauthorized_user_cannot_access_post_update(client, create_post):
        # Создаем пост и получаем его slug
        post = create_post(slug="test-post")

        # Формируем URL для обновления поста
        url = reverse("post_update", kwargs={"slug": post.slug})

        # Отправляем GET-запрос неавторизованным клиентом
        response = client.get(url)

        # Проверяем статус ответа (редирект)
        assert response.status_code == 302

        # Проверяем, что редирект ведет на страницу входа
        login_url = reverse("login")  # Замените "login" на имя вашего URL для входа
        assert response.url.startswith(login_url)

        # Проверяем наличие параметра next в URL редиректа
        assert f"next={url}" in response.url

    def test_unauthenticated_user_cannot_create_post(self):
        url = reverse('post_create')
        response = self.client.post(url, {
            'title': 'Hacked Post',
            'text': 'Malicious Content'
        })
        print(response)
        self.assertEqual(response.status_code, 403)  # 403 Forbidden
        self.assertEqual(Post.objects.count(), 1)  # Пост не создан

    # Тест 3: Автор может редактировать свой пост
    def test_author_can_update_post(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('post_update')
        response = self.client.put(url, {
            'title': 'Updated Title',
            'text': 'Updated Content'
        }, content_type='application/json')
        print(response)
        self.post.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.post.title, 'Updated Title')

    # Тест 4: Не-автор не может редактировать пост
    def test_non_author_cannot_update_post(self):
        self.client.login(username='otheruser', password='testpass456')
        url = reverse('post_update')
        response = self.client.put(url, {
            'title': 'Hacked Title',
            'text': 'Hacked Content'
        }, content_type='application/json')

        self.post.refresh_from_db()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.post.title, 'Original Title')  # Данные не изменились
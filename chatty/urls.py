#chatty/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import search_view
from posts.views import home  # импортируем наше представление

urlpatterns = [
    path('admin/', admin.site.urls), #Панель администратора Djan
    path('home/', home, name='home'), # Основная страница
    path('', include('users.urls')),  # ✅ Подключаем маршруты из `users/urls.py` регистрация, вход
    path('accounts/', include('django.contrib.auth.urls')), # Стандартные маршруты аутентификации Django

    path('posts/', include('posts.urls', namespace='posts')),# Маршруты приложения "posts" (управление публикациями)

    path('subscriptions/', include('subscriptions.urls', namespace='subscriptions')),# Маршруты приложения "subscriptions" (подписки пользователей)
    path('search/', search_view, name='search'),  #  Поиск публикаций (функция `search_results`)




]

# Добавляем поддержку медиа-файлов (аватары, изображения и т.д.)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
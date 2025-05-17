#chatty/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import search_results

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),  # ✅ Подключаем маршруты из `users/urls.py`
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('users.urls')),
    path('posts/', include('posts.urls', namespace='posts')),
    #path('posts/', include('posts.urls')),# Включаем URL-адреса приложения posts
    path('subscriptions/', include('subscriptions.urls', namespace='subscriptions')),# Включаем URL-адреса приложения subscriptions
    path('posts/search/', search_results, name='search'),  # ✅ Объявляем маршрут

]

# Добавляем поддержку медиа-файлов (аватары, изображения и т.д.)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
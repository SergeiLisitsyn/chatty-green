#chatty/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import search_view, welcome, home
from posts.views import home  # импортируем наше представление
from ads.views import home  # отсюда идет функция home()
from users import views as users_views
app_name = 'users'


urlpatterns = [

    path('admin/', admin.site.urls), #Панель администратора Djan
    path('profile/<str:username>/', users_views.profile, name='profile'),
    path('', welcome, name='welcome'),  # сначала приветствие
    path('home/', home, name='home'),  # главная страница —  с ads.views.home
    path('users/', include('users.urls')),  # все роуты users под префиксом users/
    # path('', include('users.urls')),  # ✅ Подключаем маршруты из `users/urls.py` регистрация, вход
    # path('', include('chatty.urls')),  # остальные маршруты (home, search и т.д.)
    path('ads/', include('ads.urls', namespace='ads')),    # Роуты для рекламы
    path('accounts/', include('django.contrib.auth.urls')), # Стандартные маршруты аутентификации Django
    path('posts/', include('posts.urls', namespace='posts')),# Маршруты приложения "posts" (управление публикациями)
    path('subscriptions/', include('subscriptions.urls', namespace='subscriptions')),# Маршруты приложения "subscriptions" (подписки пользователей)
    path('search/', search_view, name='search'),  #  Поиск публикаций (функция `search_results`)
    # path('', include('ads.urls')),  # главная страница теперь будет из ads.views.home


]

# Добавляем поддержку медиа-файлов (аватары, изображения и т.д.)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
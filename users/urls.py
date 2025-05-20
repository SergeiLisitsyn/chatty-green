#users/urls.py

from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView

from django.urls import reverse_lazy



urlpatterns = [
    path('', views.welcome_view, name='welcome'),  # Приветственная страница
    # path('home/', views.home_view, name='home'),  # Основная страница
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(template_name='users/login.html'), name='login'),  # используем кастомное представление
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('posts:post_list')), name='logout'),

    path('profile/<str:username>/', views.profile, name='profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),  # Добавлен путь для редактирования профиля

]

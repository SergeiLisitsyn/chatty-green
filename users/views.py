# users/views.py
from django.db.models import Count
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User

from posts.models import Post
from subscriptions.models import Subscription
from .models import CustomUser  # если переопределялась модель
from .forms import CustomUserCreationForm, CustomPasswordChangeForm  # если форма расширялась
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import CustomUserEditForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy


def welcome_view(request):
    return render(request, 'welcome.html')  # Загружаем welcome.html

def home_view(request):
    return render(request, 'home.html')  # Загружаем основную страницу (base.html)

def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile', username=user.username)
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def profile(request, username):
    # Получаем объект пользователя, чей профиль хотим показать
    profile_user = get_object_or_404(CustomUser, username=username)

    # Вычисляем статус подписки: если залогиненный пользователь подписан на профиль profile_user
    is_subscribed = False
    if request.user.is_authenticated and request.user != profile_user:
        is_subscribed = Subscription.objects.filter(
            subscriber=request.user,
            author=profile_user
        ).exists()

    # Получаем последние посты profile_user с аннотациями подсчётов лайков и комментариев
    posts_query = Post.objects.filter(author=profile_user)
    user_posts = posts_query.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True)
    ).order_by('-publication_date')[:4]

    # Определяем ID постов, которые лайкнул текущий пользователь
    user_liked_posts = []
    if request.user.is_authenticated:
        liked_post_ids = posts_query.filter(likes=request.user).values_list('id', flat=True)
        user_liked_posts = list(liked_post_ids)

    context = {
        'profile_user': profile_user,
        'is_subscribed': is_subscribed,
        'user_posts': user_posts,
        'user_liked_posts': user_liked_posts
    }
    return render(request, 'users/profile.html', context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Редиректим на страницу профиля пользователя
            return redirect('profile', username=user.username)
        else:
            messages.error(request, 'Неверный логин или пароль')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


class CustomLoginView(LoginView):
    def get_success_url(self):
        #return '/posts/create/'
        return '/posts/'  # после входа отправлять пользователя на /posts/.
        # return f'/profile/{self.request.user.username}'


def edit_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)

    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, request.FILES, instance=user)  # Используйте нужную форму
        if form.is_valid():
            form.save()
            return redirect('profile', username=user.username)
    else:
        form = CustomUserCreationForm(instance=user)  # Предзаполненная форма

    return render(request, 'users/edit_profile.html', {'form': form, 'user': user})


def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Необходимо для сохранения авторизации после смены пароля
            messages.success(request, 'Пароль был успешно изменен!')
            return redirect('profile', username=request.user.username)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'users/change_password.html', {'form': form})


class LoggingPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('password_reset_complete')

    def form_valid(self, form):
        # Логирование перед изменением пароля
        user = form.user
        print(f"\n=== DEBUG: Password Reset ===")
        print(f"User: {user.username} (ID: {user.id})")
        print(f"Old password hash: {user.password}")

        # Сохраняем старый хеш для сравнения
        old_password_hash = user.password

        # Вызываем родительский метод (который меняет пароль)
        response = super().form_valid(form)

        # Обновляем объект пользователя из БД
        user.refresh_from_db()

        # Логирование после изменения
        print(f"New password hash: {user.password}")
        print(f"Password changed: {old_password_hash != user.password}")
        print("============================\n")

        return response
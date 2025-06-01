from django.shortcuts import render
from posts.models import Post
from django.db.models import Q

from videopost.models import VideoPost


def welcome(request):
    """Отображает страницу приветствия (welcome.html)."""
    return render(request, 'welcome.html')

def home(request):
    """Отображает главную страницу."""
    return render(request, 'home.html')


def register(request):
    """Отображает страницу регистрации."""
    return render(request, "register.html")


def search_results(request):
    query = request.GET.get("q", "").strip()
    # Результаты поиска для постов (по заголовку и тексту)
    posts = Post.objects.filter(Q(title__icontains=query) | Q(text__icontains=query), is_archived=False)
    # Результаты поиска для видео (по заголовку и описанию)
    video_results = VideoPost.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query),
        is_archived=False
    )
    context = {
        'query': query,
        'post_results': posts,
        'video_results': video_results,
    }
    return render(request, "include/search_results.html", context)

def search_view(request):
    """
        ищет посты по заголовку (title) и содержанию (content). icontains
        """

    query = request.GET.get('q')  # Получаем введенный запрос
    results = Post.objects.filter(Q(title__icontains=query) | Q(text__icontains=query)) if query else None
    return render(request, 'include/search_results.html', {'results': results})



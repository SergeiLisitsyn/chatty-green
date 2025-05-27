# -- chatty/views.py
from django.shortcuts import render
from posts.models import Post
from django.db.models import Q

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
    posts = Post.objects.filter(Q(title__icontains=query) | Q(text__icontains=query), is_archived=False)

    return render(request, "posts/search_results.html", {"posts": posts, "query": query})

def search_view(request):
    """
        ищет посты по заголовку (title) и содержанию (content). icontains
        """

    query = request.GET.get('q')  # Получаем введенный запрос
    results = Post.objects.filter(Q(title__icontains=query) | Q(text__icontains=query)) if query else None
    return render(request, 'include/search_results.html', {'results': results})



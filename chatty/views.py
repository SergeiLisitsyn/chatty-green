from django.shortcuts import render
from posts.models import Post
from django.db.models import Q

def home(request):
    """Отображает главную страницу."""
    return render(request, 'home.html')


def register(request):
    """Отображает страницу регистрации."""
    return render(request, "register.html")


def search_view(request):
    """
        ищет посты по заголовку (title) и содержанию (content). icontains
        """

    query = request.GET.get('q')  # Получаем введенный запрос
    results = Post.objects.filter(Q(title__icontains=query) | Q(text__icontains=query)) if query else None
    return render(request, 'include/search_results.html', {'results': results})


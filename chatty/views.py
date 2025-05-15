from django.shortcuts import render
from posts.models import Post
from django.db.models import Q

def home(request):
    """Отображает главную страницу."""
    return render(request, 'home.html')


def register(request):
    """Отображает страницу регистрации."""
    return render(request, "register.html")


def search_results(request):
    """
        Выполняет поиск публикаций по заголовку или тексту, исключая архивированные.

        Аргументы:
        - request: объект запроса Django, содержащий параметры поиска.

        Возвращает:
        - HTML-страницу с результатами поиска.
        """
    query = request.GET.get("q", "")
    posts = Post.objects.filter(Q(title__icontains=query) | Q(text__icontains=query), is_archived=False)
    return render(request, "posts/search_results.html", {"posts": posts, "query": query})

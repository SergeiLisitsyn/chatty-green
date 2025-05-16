from django.shortcuts import render
from posts.models import Post
from django.db.models import Q

def home(request):
    return render(request, 'home.html')


def register(request):
    return render(request, "register.html")


def search_results(request):
    query = request.GET.get("q", "").strip()
    posts = Post.objects.filter(Q(title__icontains=query) | Q(text__icontains=query), is_archived=False)

    return render(request, "posts/search_results.html", {"posts": posts, "query": query})

from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail_by_slag(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

class PostDetailViewSlug(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'  # Поле модели для поиска по слагу
    slug_url_kwarg = 'slug'  # Название параметра в URL

class PostDetailViewId(DetailView):
    model = Post
    template_name = 'post_detail.html'  # Можно использовать тот же шаблон
    context_object_name = 'post'
    pk_field = 'pk'
    pk_url_kwarg = 'pk'  # Явное указание параметра URL
    print(f'pk_url_kwarg = {pk_url_kwarg}')
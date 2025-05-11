from django.urls import path
from . import views
from .views import PostUpdateView, PostDeleteView, PostCreateView, PostDetailView
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('', views.PostListView.as_view(), name='post_list'),                        # Список постов
    path('create/', PostCreateView.as_view(), name='post_create'),                   # Создание поста
    path('<slug:slug>/edit/', PostUpdateView.as_view(), name='post_edit'),           # Редактирование
    path('<slug:slug>/delete/', PostDeleteView.as_view(), name='post_delete'),       # Удаление
    path('<slug:slug>/like/', views.like_post, name='like_post'),                    # AJAX-лайк
    path('<slug:slug>/dislike/', views.dislike_post, name='dislike_post'),           # AJAX-дизлайк
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),              # Детали поста (в конце!)
]


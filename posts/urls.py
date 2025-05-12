from django.urls import path
from . import views
from .views import PostUpdateView, PostDeleteView, PostCreateView, PostDetailView, like_post, dislike_post
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from .views import FeedView


urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),                       # Список постов
    path('create/', views.PostCreateView.as_view(), name='post_create'),                # Страница создания поста
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail_by_id'),
    # path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),     # Страница детали поста
    path('<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_edit'),       # Страница редактирования поста
    path('<slug:slug>/update/', PostUpdateView.as_view(), name='post_update'),  # редактировать пост доступно только автору поста
    path('<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),    # Страница удаления поста
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),#Этот маршрут позволяет просматривать посты по их `slug`.
    path('<slug:slug>/like/', like_post, name='like_post'),  #Этот маршрут обрабатывает лайк для поста.
    path('<slug:slug>/dislike/', dislike_post, name='dislike_post'),  # ✅ Должен быть этот маршрут!
    path('feed/', FeedView.as_view(), name='feed'),
]
# posts/urls.py

from django.urls import path
from . import views
from .views import PostListView
from posts.views import archive_post


app_name = 'posts'

urlpatterns = [

    path('', views.PostListView.as_view(), name='post_list'),  # Список постов
    path('create/', views.PostCreateView.as_view(), name='post_create'),  # Создание поста
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),  # Детали поста
    path('<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_update'),  # Редактирование поста
    path('<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),  # Удаление поста
    path('<slug:slug>/archive/', archive_post, name='archive_post'),
    path('<slug:slug>/like/', views.like_post, name='like_post'),  # Лайк поста
    path('<slug:slug>/dislike/', views.dislike_post, name='dislike_post'),  # Дизлайк поста
    path('id/<int:pk>/', views.PostDetailViewId.as_view(), name='post_detail_id'),  # Детали поста по ID
]



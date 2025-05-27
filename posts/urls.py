from django.urls import path
from . import views
from .views import PostListView, archive_post, search_results

app_name = 'posts'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),  # Список постов
    path('create/', views.PostCreateView.as_view(), name='post_create'),  # Создание поста
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),  # Детали поста
    path('<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_update'),  # Редактирование поста
    path('<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),  # Удаление поста
    path('<slug:slug>/archive/', archive_post, name='archive_post'),  # Архивирование поста
    # path('<int:post_id>/like/', views.toggle_like, name='like_post'),  # ✅ Исправлено

    path('<slug:slug>/like/', views.toggle_like, name='like_post'),  # Лайк поста (только по slug)
    path('<slug:slug>/dislike/', views.dislike_post, name='dislike_post'),  # Дизлайк поста

    path('id/<int:pk>/', views.PostDetailViewId.as_view(), name='post_detail_id'),  # Детали поста по ID
    path("search/", search_results, name="search"),  # Поиск
    path('posts/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail')

]





# videopost/urls.py

from django.urls import path
from .views import reply_comment
from . import views
from .views import (
    VideoPostListView,
    VideoPostCreateView,
    VideoPostDetailView,
    VideoPostUpdateView,
    VideoPostDeleteView,
    VideoPostDetailViewId,
    VideoFeedView,
    archive_videopost,
    toggle_videolike,
    toggle_videodislike,
    search_video_results,
    videopost_api_detail,
    delete_videopost,
    # video_like,  # ✅ добавлен импорт
    # video_dislike, delete_videopost  # ✅ добавлен импорт
)

app_name = 'videopost'

urlpatterns = [
    # 1. Главный список всех видеопостов
    path('', VideoPostListView.as_view(), name='videopost_list'),

    # 2. Создание нового видеопоста
    path('create/', VideoPostCreateView.as_view(), name='videopost_create'),

    # 3. Лента подписок
    path('feed/', VideoFeedView.as_view(), name='videopost_feed'),

    # 4. Поиск по видеопостам
    path('search/', search_video_results, name='search_video'),

    # 5. Детали по ID
    path('id/<int:pk>/', VideoPostDetailViewId.as_view(), name='videopost_detail_id'),

    # 6. Редактирование
    path('<slug:slug>/edit/', VideoPostUpdateView.as_view(), name='videopost_update'),

    # 7. Удаление
    path('<slug:slug>/delete/', VideoPostDeleteView.as_view(), name='videopost_delete'),

    # 8. Архивация
    path('<slug:slug>/archive/', archive_videopost, name='archive_videopost'),

    # 9. Лайк через AJAX
    path('<slug:slug>/like/', toggle_videolike, name='like_videopost'),

    # 10. Дизлайк через AJAX
    path('<slug:slug>/dislike/', toggle_videodislike, name='dislike_videopost'),

    # 11. API-детали
    path('api/<slug:slug>/', videopost_api_detail, name='videopost_api_detail'),

    # 12. Детали по slug (основной путь)
    path('<slug:slug>/', VideoPostDetailView.as_view(), name='videopost_detail'),

    # 13. Альтернативный путь для детализации
    path('video/<slug:slug>/', VideoPostDetailView.as_view(), name='video_detail'),

    # 14. Лайк/дизлайк через POST-запросы (альтернативный путь)
    path('video/<slug:slug>/like/', toggle_videolike, name='video_like'),
    path('video/<slug:slug>/dislike/', toggle_videodislike, name='video_dislike'),

    path('<slug:slug>/ajax-delete/', delete_videopost, name='ajax_delete_videopost'),
    path('comment/<int:comment_id>/reply/', reply_comment, name='reply_comment'),

    path('share/', views.share_videopost, name='share_videopost'),

]

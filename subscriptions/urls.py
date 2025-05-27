#  subscriptions/urls.py
from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [

    path('toggle/<str:username>/', views.SubscriptionToggleView.as_view(), name='toggle'), # Подписаться/отписаться от пользователя
    path('followers/<str:username>/', views.FollowersListView.as_view(), name='followers'),  # Список подписчиков пользователя
    path('following/<str:username>/', views.FollowingListView.as_view(), name='following'), # Список подписок пользователя
    path('feed/', views.FeedView.as_view(), name='feed'),
]
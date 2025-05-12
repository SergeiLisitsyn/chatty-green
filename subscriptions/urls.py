from django.urls import path
from .views import SubscribeView

urlpatterns = [
    path('subscribe/<int:author_id>/', SubscribeView.as_view(), name='subscribe'),
]
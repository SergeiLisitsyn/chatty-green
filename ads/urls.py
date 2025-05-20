# ads/urls.py

from django.urls import path
from .views import create_advertisement, advertisement_list

app_name = 'ads'

urlpatterns = [
    path('', advertisement_list, name='list'),  # Главная страница рекламы: /ads/
    path('create/', create_advertisement, name='create'),  # Страница создания рекламы: /ads/create/
]

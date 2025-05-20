from django.urls import path
from .views import home, create_advertisement
from .views import advertisement_list



app_name = 'ads'  # ← это обязательно, при использовании namespace в include()

urlpatterns = [
    path('', home, name='home'),
    path('', advertisement_list, name='list'),
    path('create/', create_advertisement, name='create'),  # ← новая форма
]

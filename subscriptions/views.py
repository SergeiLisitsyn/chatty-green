from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Subscription
from django.contrib.auth import get_user_model

class SubscribeView(LoginRequiredMixin, View):
    def post(self, request, author_id):
        # Получаем автора по его ID
        author = get_user_model().objects.get(id=author_id)
        # Пытаемся получить или создать подписку
        subscription, created = Subscription.objects.get_or_create(
            subscriber=request.user,
            author=author
        )
        # Если подписка уже существует, удаляем ее (отписка)
        if not created:
            subscription.delete()
            subscribed = False
        else:
            subscribed = True
        # Возвращаем JSON-ответ с информацией о подписке
        return JsonResponse({'subscribed': subscribed})
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Subscription
from django.contrib.auth import get_user_model

class SubscribeView(LoginRequiredMixin, View):
    def post(self, request, author_id):
        author = get_user_model().objects.get(id=author_id)
        subscription, created = Subscription.objects.get_or_create(
            subscriber=request.user,
            author=author
        )
        if not created:
            subscription.delete()
            subscribed = False
        else:
            subscribed = True
        return JsonResponse({'subscribed': subscribed})
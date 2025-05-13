from django.contrib import admin
from .models import Subscription

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'author', 'created_at')
    list_filter = ('subscriber', 'author', 'created_at')
    search_fields = ('subscriber__username', 'author__username')


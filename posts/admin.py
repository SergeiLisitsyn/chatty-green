from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','author', 'publication_date', 'slug')
    search_fields = ('text', 'title', 'author__username')
    list_filter = ('publication_date',)
    actions = ['mark_deleted']


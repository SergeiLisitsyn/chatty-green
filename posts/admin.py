from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','author', 'publication_date', 'slug')
    search_fields = ('text', 'title', 'author__username')
    list_filter = ('publication_date',)
    actions = ['mark_deleted']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text','author', 'created_at')
    search_fields = ('text', 'author', 'created_at')
    list_filter = ('author',)

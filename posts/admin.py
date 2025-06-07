# posts/admin.py

from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if 'image' in form.changed_data:
            storage = default_storage
            obj.image.name = storage.save(f'post_images/{obj.image.name}', obj.image.file)
        super().save_model(request, obj, form, change)

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

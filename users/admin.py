
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_banned', 'banned_until', 'is_staff')
    list_filter = ('is_banned', 'is_staff', 'is_superuser')
    actions = ['ban_users', 'unban_users']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email', 'avatar', 'bio', 'contacts')}),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Бан', {
            'fields': ('is_banned', 'ban_reason', 'banned_until'),
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    def ban_users(self, request, queryset):
        queryset.update(is_banned=True)

    ban_users.short_description = "Забанить выбранных пользователей"

    def unban_users(self, request, queryset):
        queryset.update(is_banned=False, ban_reason=None, banned_until=None)

    unban_users.short_description = "Разбанить выбранных пользователей"


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_banned_status')

    def get_banned_status(self, obj):
        return obj.user.is_banned

    get_banned_status.short_description = 'Статус бана'
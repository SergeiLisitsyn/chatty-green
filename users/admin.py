
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('avatar', 'bio', 'contacts')}),
    )

# Фильтр для бана
class BannedFilter(admin.SimpleListFilter):
    title = 'Бан'
    parameter_name = 'is_banned'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Забаненные'),
            ('no', 'Не забаненные'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(profile__is_banned=True)
        if self.value() == 'no':
            return queryset.filter(profile__is_banned=False)

# Inline для профиля
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

# Кастомный UserAdmin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'is_banned', 'is_staff')
    list_filter = (BannedFilter, 'is_staff', 'is_superuser')
    actions = ['ban_users', 'unban_users']

    def is_banned(self, obj):
        return obj.profile.is_banned
    is_banned.boolean = True

    def ban_users(self, request, queryset):
        for user in queryset:
            user.profile.is_banned = True
            user.profile.save()
    ban_users.short_description = "Забанить"

    def unban_users(self, request, queryset):
        for user in queryset:
            user.profile.is_banned = False
            user.profile.save()
    unban_users.short_description = "Разбанить"


admin.site.register(CustomUser, CustomUserAdmin)

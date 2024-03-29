from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from accounts import models
from accounts.forms import UserAccountChangeForm


class UserAccountAdmin(BaseUserAdmin):
    form = UserAccountChangeForm
    fieldsets = (
        (None, {'fields': ('username', 'email', 'role', 'password', 'creator')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'role', 'creator')
    list_filter = ('role', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(models.UserAccount, UserAccountAdmin)


admin.site.register(models.IPAddress)
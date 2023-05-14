"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name', 'image')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'image',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )

class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'due_date', 'priority', 'created_at', 'updated_at']
    list_filter = ['category', 'due_date', 'priority', 'created_at', 'updated_at']
    search_fields = ['title', 'user']


class SubtaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'done', 'created_at', 'updated_at']
    list_filter = ['done', 'created_at', 'updated_at']
    search_fields = ['title', 'user']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'color', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name']

class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_number', 'user', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'email']


class ListAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'board', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name']


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.Subtask, SubtaskAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Board)
admin.site.register(models.List, ListAdmin)
admin.site.register(models.Contact, ContactAdmin)
admin.site.register(models.Summary)

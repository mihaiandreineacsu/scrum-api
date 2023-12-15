"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering = ["id"]
    list_display = ["email", "name"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ("name", "image")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    readonly_fields = ["last_login"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "image",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


admin.site.register(models.User, UserAdmin)


class TaskAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = [
        "id",
        "title",
        "user",
        "category",
        "due_date",
        "priority",
        "created_at",
        "updated_at",
        "position",
    ]
    list_filter = [
        "category",
        "due_date",
        "priority",
        "created_at",
        "updated_at",
        "user",
        "position",
    ]
    search_fields = ["title", "user"]


admin.site.register(models.Task, TaskAdmin)


class SubtaskAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["id", "title", "user", "done", "created_at", "updated_at"]
    list_filter = ["done", "created_at", "updated_at", "user"]
    search_fields = ["title", "user"]


admin.site.register(models.Subtask, SubtaskAdmin)


class BoardAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["id", "title", "user", "created_at", "updated_at"]
    list_filter = ["user", "created_at", "updated_at"]
    search_fields = ["title", "user"]


admin.site.register(models.Board, BoardAdmin)


class CategoryAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["id", "name", "user", "color", "created_at", "updated_at"]
    list_filter = ["created_at", "updated_at", "user"]
    search_fields = ["name", "user"]


admin.site.register(models.Category, CategoryAdmin)


class ContactAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = [
        "id",
        "name",
        "email",
        "phone_number",
        "user",
        "created_at",
        "updated_at",
    ]
    list_filter = ["created_at", "updated_at", "user"]
    search_fields = ["name", "email", "user"]


admin.site.register(models.Contact, ContactAdmin)


class ListAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = [
        "id",
        "name",
        "user",
        "board",
        "created_at",
        "updated_at",
        "position",
    ]
    list_filter = ["created_at", "updated_at", "user", "position"]
    search_fields = ["name", "user"]


admin.site.register(models.List, ListAdmin)


class SummaryAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["id", "created_at", "updated_at", "user"]
    list_filter = ["created_at", "updated_at", "user"]
    search_fields = ["user"]


admin.site.register(models.Summary, SummaryAdmin)

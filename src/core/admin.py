"""
Django admin customization.
"""

from typing import override
from django.http.request import HttpRequest
from ordered_model.admin import (
    OrderedStackedInline,
    OrderedInlineModelAdminMixin,
)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


@admin.register(models.User)
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


class BoardListsOfTasksInLine(OrderedStackedInline):
    model = models.ListOfTasks
    fields = (
        "name",
        "move_up_down_links",
    )
    readonly_fields = ("move_up_down_links",)
    ordering = ("order",)
    extra = 0


@admin.register(models.Board)
class BoardAdmin(OrderedInlineModelAdminMixin, admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["id", "title", "user", "created_at", "updated_at"]
    list_filter = ["user", "created_at", "updated_at"]
    search_fields = ["title", "user"]
    inlines = (BoardListsOfTasksInLine,)

    def save_formset(
        self,
        request: HttpRequest,
        form: models.Any,
        formset: models.Any,
        change: models.Any,
    ) -> None:
        return super().save_formset(request, form, formset, change)


class ListsOfTaskTasksInline(OrderedStackedInline):
    model = models.Task
    fields = (
        "title",
        "description",
        "due_date",
        "priority",
        "move_up_down_links",
    )
    readonly_fields = ("move_up_down_links",)
    ordering = ("order",)
    extra = 0


@admin.register(models.ListOfTasks)
class ListAdmin(OrderedInlineModelAdminMixin, admin.ModelAdmin):
    ordering = ["id"]
    list_display = [
        "id",
        "name",
        "board",
        "created_at",
        "updated_at",
        "order",
    ]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["name", "user"]
    readonly_fields = ["order"]
    inlines = (ListsOfTaskTasksInline,)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["id", "name", "user", "color", "created_at", "updated_at"]
    list_filter = ["created_at", "updated_at", "user"]
    search_fields = ["name", "user"]


@admin.register(models.Contact)
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


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = [
        "id",
        "title",
        "category",
        "due_date",
        "priority",
        "created_at",
        "updated_at",
        "order",
    ]
    list_filter = [
        "category",
        "due_date",
        "priority",
        "created_at",
        "updated_at",
        "order",
    ]
    search_fields = ["title", "user"]


@admin.register(models.Subtask)
class SubtaskAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["id", "title", "done", "created_at", "updated_at"]
    list_filter = ["done", "created_at", "updated_at"]
    search_fields = ["title"]


# class SummaryAdmin(admin.ModelAdmin):
#     ordering = ["id"]
#     list_display = ["id", "created_at", "updated_at", "user"]
#     list_filter = ["created_at", "updated_at", "user"]
#     search_fields = ["user"]
# admin.site.register(models.Summary, SummaryAdmin)

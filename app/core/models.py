"""
Database models.
"""
import uuid
import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from colorfield.fields import ColorField


def user_image_file_path(instance, filename):
    """Generate file path for new user image."""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"

    return os.path.join("uploads", "user", filename)


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    `created_at` and `updated_at` fields.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    image = models.ImageField(null=True, upload_to=user_image_file_path)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Board(TimeStampedModel):
    """Board Object."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255, default="Untitled")

    def __str__(self):
        return self.title


class List(TimeStampedModel):
    """List Object."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255, default="Untitled")
    board = models.ForeignKey(
        Board, on_delete=models.SET_NULL, null=True, blank=True, related_name="lists"
    )
    position = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["board", "position"], name="unique_position_per_board"
            )
        ]

    @staticmethod
    def swap_positions(list1, list2):
        if list1.board != list2.board:
            raise ValueError("Lists are not in the same board")

        # Use a temporary position that is not likely to conflict
        temporary_position = -1  # or another value that you're sure won't conflict
        list1_position = list1.position
        list2_position = list2.position
        list1.position, list2.position = temporary_position, list1_position
        list1.save()
        list2.save()

        # Finally, assign the original list2's position to list1
        list1.position = list2_position
        list1.save()


class Contact(TimeStampedModel):
    """Contact object"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(TimeStampedModel):
    """Category Object"""

    class Meta:
        verbose_name_plural = "Categories"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    color = ColorField(default="#FFF0000")

    def __str__(self):
        return self.name


class Task(TimeStampedModel):
    """Task object."""

    PRIORITY_CHOICES = [("Urgent", "Urgent"), ("Medium", "Medium"), ("Low", "Low")]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    assignees = models.ManyToManyField(Contact, blank=True, related_name="assignees")
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="Low")
    list = models.ForeignKey(
        List, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks"
    )
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.title


class Subtask(TimeStampedModel):
    """Subtask object."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="subtasks")
    title = models.CharField(max_length=255)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Summary(TimeStampedModel):
    """Summary object"""

    class Meta:
        verbose_name_plural = "Summaries"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

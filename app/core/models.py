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
from django.contrib.postgres.fields import ArrayField
from datetime import date, datetime
from colorfield.fields import ColorField


def user_image_file_path(instance, filename):
    """Generate file path for new user image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'user', filename)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
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


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    image = models.ImageField(null=True, upload_to=user_image_file_path)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Category(models.Model):
    """Category Object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    color = ColorField(default="#FFF0000")
    def __str__(self):
        return self.name



class Board(models.Model):
    """Board Object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateField(default=datetime.now)
    def __str__(self):
        return self.created_at


class Contact(models.Model):
    """Contact object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)


class Subtask(models.Model):
    """Subtask object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    done = models.BooleanField(default=False)
    def __str__(self):
        return self.title


class Task(models.Model):
    """Task object."""

    PRIORITY_CHOICES = [('Urgent', 'Urgent'), ('Medium', 'Medium'), ('Low', 'Low')]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    assignees = models.ManyToManyField(Contact, default=list, blank=True, related_name='assignees')
    subtasks = models.ManyToManyField(Subtask, default=list, blank=True, related_name='subtasks')
    due_date = models.DateField(null=False, blank=False)
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default='Low')

    def __str__(self):
        return self.title


class Summary(models.Model):
    """Summary object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

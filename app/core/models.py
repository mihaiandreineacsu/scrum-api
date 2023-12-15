"""
Database models.
"""
import uuid
import os
from django.conf import settings
from django.db import models, transaction
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


class PositionedModel(models.Model):
    """Abstract model to handle position-related functionality."""

    position = models.IntegerField(null=True)
    parent_attribute = None  # This will be set in the subclasses

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(fields=["position"], name="unique_position")
        ]

    @classmethod
    def swap_positions(cls, instance1, instance2):
        print("Swap positions, task 1 {}, task 2 {}".format(instance1, instance2))
        if not cls.parent_attribute:
            raise ValueError(f"parent_attribute is not set in {cls.__name__}")

        if instance1.__class__ != instance2.__class__:
            raise ValueError("Instances are not of the same class")

        # Check if both instances belong to the same parent entity
        parent1 = getattr(instance1, cls.parent_attribute)
        parent2 = getattr(instance2, cls.parent_attribute)

        with transaction.atomic():
            # Swap positions
            temporary_position = (
                None  # or another value that you're sure won't conflict
            )
            instance1_position = instance1.position
            instance2_position = instance2.position
            instance1.position = temporary_position

            if parent1 != parent2:
                if instance1_position == instance2_position:
                    pass
                setattr(instance1, cls.parent_attribute, parent2)
            # raise ValueError("Instances are not in the same parent entity")
            instance1.save()

            # Determine direction and range for shifting positions
            if instance1_position < instance2_position:
                # Shift positions of instances between instance1 and instance2 down by one
                instances_between = cls.objects.filter(
                    **{cls.parent_attribute: parent1},
                    position__gt=instance1_position,
                    position__lt=instance2_position,
                ).order_by('position')  # Sorting in ascending order

                instances_between.update(position=models.F("position") - 1)
                instance2.position = instance2_position - 1
            elif instance1_position > instance2_position:
                # Shift positions of instances between instance2 and instance1 up by one
                instances_between = cls.objects.filter(
                    **{cls.parent_attribute: parent1},
                    position__lt=instance1_position,
                    position__gt=instance2_position,
                ).order_by('-position')  # Sorting in descending order

                instances_between.update(position=models.F("position") + 1)
                instance2.position = instance2_position + 1
            else:
                pass
            instance2.save()
            # Move instance1 to instance2's position
            instance1.position = instance2_position
            instance1.save()

    def __str__(self):
        return str(self.position)


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


class List(TimeStampedModel, PositionedModel):
    """List Object."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255, default="Untitled")
    board = models.ForeignKey(
        Board, on_delete=models.SET_NULL, null=True, blank=True, related_name="lists"
    )
    parent_attribute = "board"  # Set the parent attribute for List

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["board", "position"], name="unique_position_per_board"
            )
        ]


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


class Task(TimeStampedModel, PositionedModel):
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

    parent_attribute = "list"  # Set the parent attribute for List

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["list", "position"], name="unique_position_per_list"
            )
        ]

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

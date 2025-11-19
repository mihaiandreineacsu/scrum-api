# pyright: reportUninitializedInstanceVariable=false

"""
Database models.
"""

import os
import uuid
from datetime import date, datetime, timedelta
from typing import TYPE_CHECKING, Any, Literal, override

from colorfield.fields import ColorField
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.db.models.constraints import CheckConstraint, UniqueConstraint
from django.db.models.expressions import Combinable
from django.utils import timezone
from ordered_model.models import OrderedModel
from phonenumber_field.modelfields import PhoneNumberField

from core.utils import PRIORITY_CHOICES, generate_name
from core.validators import (
    DEFAULT_TEXT_FIELD_MAX_LENGTH,
    DEFAULT_TEXT_FIELD_MIN_LENGTH,
    EMAIL_REGEX,
    SPACING_REGEX,
    char_length_validator,
    choice_validator,
    email_validator,
    generate_choice_regex,
    generate_length_regex,
    spacing_validator,
    text_length_validator,
)


def default_due_date() -> date:
    return (timezone.now() + timedelta(days=7)).date()


# TODO: limit the image to size and extension
# Also when user gets deleted, delete the image
# Also when user image is updated / cleared, delete the old image
def user_image_file_path(_: models.Model | None, filename: str) -> str:
    """Generate file path for new user image."""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    return os.path.join("uploads", "user", filename)


class TimeStampedModel(models.Model):
    """Abstract base class that adds created_at and updated_at fields to models."""

    if TYPE_CHECKING:
        created_at: models.DateTimeField[datetime, datetime]
        updated_at: models.DateTimeField[datetime, datetime]
    else:
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract: bool = True


if TYPE_CHECKING:
    UserBasedManager = BaseUserManager["User"]
else:
    UserBasedManager = BaseUserManager


class CustomUserManager(UserBasedManager):
    """Manager for users."""

    def create_user(
        self, email: str, password: str | None = None, **extra_fields: Any
    ) -> "User":
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must have an email address.")
        user = User(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email: str, password: str) -> "User":
        """Create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

    def create_guest_user(self, **extra_fields: Any) -> "User":
        """Create and return a new guest user with a random username."""
        random_identifier = generate_name()
        dummy_email = f"{self.normalize_email_identifier(random_identifier)}@guest.com"
        user = User(email=dummy_email, **extra_fields)
        user.name = f"{random_identifier}"
        user.set_unusable_password()
        user.is_guest = True
        user.save(using=self._db)
        return user

    def normalize_email_identifier(self, identifier: str) -> str:
        """Lowercases a string and replaces spaces with underscore"""
        normalized = identifier.lower()
        normalized = normalized.replace(" ", "_")
        return normalized


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """User in the system."""

    if TYPE_CHECKING:
        email: models.EmailField[str, str]
        name: models.CharField[str, str]
        is_active: bool | models.BooleanField[bool | Combinable, bool]
        is_staff: models.BooleanField[bool, bool]
        image: models.ImageField
        is_guest: models.BooleanField[bool, bool]
        is_superuser: models.BooleanField[bool, bool]

    USERNAME_FIELD: Literal["email"] = "email"

    email = models.EmailField(
        unique=True,
        validators=[
            email_validator(
                code="%(app_label)s_%(class)s_email_invalid",
            ),
            char_length_validator(
                code="%(app_label)s_%(class)s_email_length_invalid",
            ),
        ],
    )
    name = models.CharField(
        default="Unnamed",
        validators=[
            char_length_validator(
                code="%(app_label)s_%(class)s_name_length_invalid",
            ),
            spacing_validator(
                code="%(app_label)s_%(class)s_name_spacing_invalid",
            ),
        ],
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True, upload_to=user_image_file_path)
    is_guest = models.BooleanField(default=False)
    objects: CustomUserManager = CustomUserManager()

    class Meta:
        constraints: list[CheckConstraint] = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_name_check",
                condition=(
                    models.Q(name__regex=generate_length_regex())
                    & ~models.Q(name__regex=SPACING_REGEX)
                ),
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_email_check",
                condition=(
                    models.Q(email__regex=EMAIL_REGEX)
                    & models.Q(email__regex=generate_length_regex())
                ),
            ),
        ]


class Board(TimeStampedModel):
    """Board Object."""

    if TYPE_CHECKING:
        user: models.ForeignKey[User, User]
        title: models.CharField[str, str]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        default="Untitled",
        validators=[
            spacing_validator(code="%(app_label)s_%(class)s_title_spacing_invalid"),
            char_length_validator(code="%(app_label)s_%(class)s_title_length_invalid"),
        ],
    )

    class Meta:
        constraints: list[CheckConstraint] = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_title_check",
                condition=(
                    models.Q(title__regex=generate_length_regex())
                    & ~models.Q(title__regex=SPACING_REGEX)
                ),
            ),
        ]

    @override
    def __str__(self) -> str:
        return f"{self.title}"


class ListOfTasks(OrderedModel, TimeStampedModel):
    """ListOfTasks Object."""

    if TYPE_CHECKING:
        name: models.CharField[str, str]
        board: models.ForeignKey[Board, Board]

    @property
    def user(self) -> User:
        return self.board.user

    @user.setter
    def user(self, value: User):
        self.board.user = value
        self.board.save()

    name = models.CharField(
        default="Unnamed",
        validators=[
            char_length_validator(code="%(app_label)s_%(class)s_name_length_invalid"),
            spacing_validator(code="%(app_label)s_%(class)s_name_spacing_invalid"),
        ],
    )
    board = models.ForeignKey(
        Board,
        on_delete=models.PROTECT,
        related_name="lists_of_tasks",
    )
    order_with_respect_to: str = "board"

    class Meta(OrderedModel.Meta):
        verbose_name_plural: str = "ListsOfTasks"
        constraints: list[UniqueConstraint | CheckConstraint] = [
            models.UniqueConstraint(
                fields=["board", "order"], name="unique_order_per_board"
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_name_check",
                condition=(
                    models.Q(name__regex=generate_length_regex())
                    & ~models.Q(name__regex=SPACING_REGEX)
                ),
            ),
        ]

    @override
    def __str__(self) -> str:
        return f"{self.name}"


class Category(TimeStampedModel):
    """Category Object"""

    if TYPE_CHECKING:
        user: models.ForeignKey[User, User]
        name: models.CharField[str, str]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        default="Issue",
        validators=[
            spacing_validator(code="%(app_label)s_%(class)s_name_spacing_invalid"),
            char_length_validator(code="%(app_label)s_%(class)s_name_length_invalid"),
        ],
    )
    color: ColorField = ColorField(default="#FFF0000")  # TODO: add color validator

    class Meta:
        verbose_name_plural: str = "Categories"
        constraints: list[UniqueConstraint | CheckConstraint] = [
            models.UniqueConstraint(
                fields=["user", "name"], name="unique_name_per_user"
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_name_check",
                condition=(
                    models.Q(name__regex=generate_length_regex())
                    & ~models.Q(name__regex=SPACING_REGEX)
                ),
            ),
        ]

    @override
    def __str__(self) -> str:
        return f"{self.name}"


class Contact(TimeStampedModel):
    """Contact object"""

    if TYPE_CHECKING:
        user: models.ForeignKey[User, User]
        name: models.CharField[str, str]
        email: models.EmailField[str, str]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    email = models.EmailField(
        default="",
        blank=True,
        validators=[
            email_validator(code="%(app_label)s_%(class)s_email_invalid"),
        ],
    )
    name = models.CharField(
        default="Anonymous",
        blank=True,
        validators=[
            spacing_validator(code="%(app_label)s_%(class)s_name_spacing_invalid"),
            char_length_validator(code="%(app_label)s_%(class)s_name_length_invalid"),
        ],
    )
    phone_number = PhoneNumberField(blank=True)

    class Meta:
        constraints: list[UniqueConstraint | CheckConstraint] = [
            models.UniqueConstraint(
                fields=["user", "email"],
                name="%(app_label)s_%(class)s_user_email_unique",
                condition=~models.Q(email__exact=""),
            ),
            models.UniqueConstraint(
                fields=["user", "phone_number"],
                name="%(app_label)s_%(class)s_user_phone_unique",
                condition=~models.Q(phone_number__exact=""),
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_email_check",
                condition=models.Q(email="") | models.Q(email__regex=EMAIL_REGEX),
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_name_check",
                condition=models.Q(name="")
                | (
                    models.Q(name__regex=generate_length_regex())
                    & ~models.Q(name__regex=SPACING_REGEX)
                ),
            ),
            # TODO add phone number check
        ]

    @override
    def __str__(self) -> str:
        return f"{self.name or self.email or self.phone_number} - {self.pk}"


class Task(OrderedModel, TimeStampedModel):
    """Task object."""

    if TYPE_CHECKING:
        title: models.CharField[str, str]
        description: models.TextField[str, str]
        category: models.ForeignKey[Category, Category]
        assignees: models.ManyToManyField[Contact, Any]
        due_date: models.DateField[date, date]
        priority: models.CharField[str, str]
        list_of_tasks: models.ForeignKey[ListOfTasks, ListOfTasks]

    @property
    def user(self) -> User:
        return self.list_of_tasks.user

    @user.setter
    def user(self, value: User):
        self.list_of_tasks.user = value
        self.list_of_tasks.save()

    title = models.CharField(
        default="Untitled",
        validators=[
            spacing_validator(code="%(app_label)s_%(class)s_title_spacing_invalid"),
            char_length_validator(code="%(app_label)s_%(class)s_title_length_invalid"),
        ],
    )
    description = models.TextField(
        blank=True,
        validators=[
            text_length_validator(
                code="%(app_label)s_%(class)s_description_length_invalid"
            )
        ],
    )
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    assignees = models.ManyToManyField(Contact, blank=True, related_name="tasks")
    due_date = models.DateField(default=default_due_date)
    priority = models.CharField(
        choices=PRIORITY_CHOICES,
        default="Low",
        validators=[
            choice_validator(
                choices=PRIORITY_CHOICES,
                code="%(app_label)s_%(class)s_priority_choice_invalid",
            )
        ],
    )
    list_of_tasks = models.ForeignKey(
        ListOfTasks,
        on_delete=models.PROTECT,
        related_name="tasks",
    )

    order_with_respect_to: str = "list_of_tasks"

    class Meta(OrderedModel.Meta):
        constraints: list[UniqueConstraint | CheckConstraint] = [
            models.UniqueConstraint(
                fields=["list_of_tasks", "order"], name="unique_order_per_list"
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_title_check",
                condition=(
                    models.Q(title__regex=generate_length_regex())
                    & ~models.Q(title__regex=SPACING_REGEX)
                ),
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_priority_check",
                condition=models.Q(
                    priority__regex=generate_choice_regex(PRIORITY_CHOICES)
                ),
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_description_check",
                condition=models.Q(description="")
                | models.Q(
                    description__regex=generate_length_regex(
                        min_length=DEFAULT_TEXT_FIELD_MIN_LENGTH,
                        max_length=DEFAULT_TEXT_FIELD_MAX_LENGTH,
                    )
                ),
            ),
        ]

    @override
    def __str__(self) -> str:
        return f"{self.title}"


class Subtask(TimeStampedModel):
    """Subtask object."""

    if TYPE_CHECKING:
        task: models.ForeignKey[Task, Task]
        title: models.CharField[str, str]
        done: models.BooleanField[bool, bool]

    @property
    def user(self) -> User:
        return self.task.user

    @user.setter
    def user(self, value: User):
        self.task.user = value
        self.task.save()

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="subtasks")
    title = models.CharField(
        default="Untitled",
        validators=[
            spacing_validator(code="%(app_label)s_%(class)s_title_spacing_invalid"),
            char_length_validator(code="%(app_label)s_%(class)s_title_length_invalid"),
        ],
    )
    done = models.BooleanField(default=False)

    class Meta:
        constraints: list[CheckConstraint] = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_title_check",
                condition=(
                    models.Q(title__regex=generate_length_regex())
                    & ~models.Q(title__regex=SPACING_REGEX)
                ),
            ),
        ]

    @override
    def __str__(self) -> str:
        return f"{self.title}"


ScrumAPIModel = Board | Category | Contact | ListOfTasks | Subtask | Task

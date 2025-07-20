"""
Tests for models.
"""

from datetime import date
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from core import models


def create_user(email="user@example.com", password="testpass123"):
    """Create and return a new user"""
    return get_user_model().objects.create_user(email, password)


def create_superuser(email="user@example.com", password="testpass123"):
    """Create and return a new user"""
    return get_user_model().objects.create_superuser(email, password)


def create_category(user, name="Category", color="#FF0000"):
    """Create and return a new category"""
    return models.Category.objects.create(user=user, name=name, color=color)


def create_contact(
    user, email="contact@example.com", name="test", phone_number="01573333333"
):
    """Create and return a new contact"""
    defaults = {
        "user": user,
        "email": email,
        "name": name,
        "phone_number": phone_number,
    }
    return models.Contact.objects.create(**defaults)


def create_task(user, **params):
    """Create and return a sample task."""
    defaults = {
        "title": "Sample task title",
        "description": "Sample description",
        "priority": "Low",
        "due_date": date.today(),
        "category": create_category(user=user),
        "priority": "Low",
    }
    defaults.update(params)

    task = models.Task.objects.create(user=user, **defaults)
    return task


def create_subtask(user, **params):
    """Create and return a sample subtask"""
    defaults = {
        "title": "Some Subtask",
        "done": False,
        "task": create_task(user=user),
    }
    defaults.update(params)
    subtask = models.Subtask.objects.create(user=user, **defaults)
    return subtask


def create_list(user, **params):
    """Create and return a sample list"""
    defaults = {
        "name": "Some List  Name",
    }
    defaults.update(params)
    list = models.List.objects.create(user=user, **defaults)
    return list


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = "test@example.com"
        password = "testpass123"
        user = create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.com", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]
        for email, expected in sample_emails:
            user = create_user(email)
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            create_user(email="")

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = create_superuser()

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    @patch("core.models.uuid.uuid4")
    def test_user_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = "test-uuid"
        mock_uuid.return_value = uuid
        file_path = models.user_image_file_path(None, "example.jpg")

        self.assertEqual(file_path, f"uploads/user/{uuid}.jpg")

    def test_create_category(self):
        """Test creating a category is successful"""
        user = create_user()
        category = create_category(user)

        self.assertEqual(str(category), category.name)

    def test_create_contact_with_email_successful(self):
        """Test creating a contact with an email is successful."""
        user = create_user()
        email = "test@example.com"
        contact = create_contact(user=user, email=email)

        self.assertEqual(contact.email, email)

    def test_create_task(self):
        """Test creating a task is successful."""
        user = create_user()
        task = create_task(user)

        self.assertEqual(str(task), task.title)

    def test_create_sub_task(self):
        """Test creating a sub task is successful."""
        user = create_user()
        sub_task = create_subtask(user=user)

        self.assertEqual(str(sub_task), sub_task.title)

    def test_create_list(self):
        """Test creating a list is successful."""
        user = create_user()
        list = create_list(user=user)
        self.assertEqual(str(list), list.name)

    def test_create_board(self):
        """Test creating a board is successful."""
        user = create_user()
        board = models.Board.objects.create(user=user)

        self.assertNotEquals(board, None)

    # def test_create_summary(self):
    #     """Test creating a summary is successful."""
    #     user = create_user()
    #     summary = models.Summary.objects.create(user=user)

    #     self.assertNotEquals(summary, None)

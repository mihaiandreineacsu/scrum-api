"""
Tests for models.
"""
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a new user"""
    return get_user_model().objects.create_user(email, password)


def create_superuser(email='user@example.com', password='testpass123'):
    """Create and return a new user"""
    return get_user_model().objects.create_superuser(email, password)


def create_task(user,
    title='Sample task title.',
    description='Sample task description.',
    priority='Low'):
    """Create and return a new Task"""
    return models.Task.objects.create(
            user=user,
            title=title,
            description=description,
            priority=priority,
        )


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = create_user(email)
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            create_user(email='')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = create_superuser()

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_task(self):
        """Test creating a task is successful."""
        user = create_user()
        task = create_task(user)

        self.assertEqual(str(task), task.title)

    @patch('core.models.uuid.uuid4')
    def test_user_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.user_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/user/{uuid}.jpg')

    def test_create_sub_task(self):
        """Test creating a sub task is successful."""
        user = create_user()
        sub_task = models.Subtask.objects.create(title='Some Subtask')

        self.assertEqual(str(sub_task), sub_task.title)

    def test_create_board(self):
        """Test creating a board is successful."""
        user = create_user()
        board = models.Board.objects.create(user=user)

        self.assertNotEquals(board, None)

    def test_create_summary(self):
        """Test creating a summary is successful."""
        user = create_user()
        summary = models.Summary.objects.create(user=user)

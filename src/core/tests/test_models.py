"""
Tests for models.
"""

import os
from unittest.mock import MagicMock, patch

from django.test import TestCase

from core import models
from core.tests.utils import (
    TEST_CONTACT_EMAIL,
    create_test_board,
    create_test_category,
    create_test_contact,
    create_test_guestuser,
    create_test_list_of_tasks,
    create_test_subtask,
    create_test_superuser,
    create_test_task,
    create_test_user,
)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = "test@example.com"
        password = "testpass123"
        user = create_test_user(
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
            user = create_test_user(email)
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            _ = create_test_user(email="")

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = create_test_superuser()

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_guestuser(self):
        """Test creating a guest."""
        user = create_test_guestuser()

        self.assertTrue(user.is_guest)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    # TODO: test guest user

    @patch("core.models.uuid.uuid4")
    def test_user_file_name_uuid(self, mock_uuid: MagicMock):
        """Test generating image path."""
        uuid = "test-uuid"
        mock_uuid.return_value = uuid
        file_path = models.user_image_file_path(None, "example.jpg")
        expected_path = os.path.join("uploads", "user", f"{uuid}.jpg")
        self.assertEqual(file_path, expected_path)

    def test_create_board(self):
        """Test creating a board is successful."""
        board = create_test_board()

        self.assertEqual(str(board), board.title)

    def test_create_list(self):
        """Test creating a list is successful."""
        list_of_tasks = create_test_list_of_tasks()

        self.assertEqual(str(list_of_tasks), list_of_tasks.name)

    def test_create_contact_successful(self):
        """Test creating a contact is successful."""
        contact = create_test_contact()

        self.assertEqual(contact.email, TEST_CONTACT_EMAIL)
        self.assertEqual(str(contact), f"{contact.name} - {contact.pk}")

    def test_create_category(self):
        """Test creating a category is successful"""
        category = create_test_category()

        self.assertEqual(str(category), category.name)

    def test_create_task(self):
        """Test creating a task is successful."""
        task = create_test_task()

        self.assertEqual(str(task), task.title)

    def test_create_sub_task(self):
        """Test creating a sub task is successful."""
        subtask = create_test_subtask()

        self.assertEqual(str(subtask), subtask.title)

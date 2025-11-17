"""
Tests for the Django admin modifications.
"""

from typing import override

from django.test import Client, TestCase
from django.urls import reverse

from core.models import User
from core.tests.utils import create_test_superuser, create_test_user


class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    admin_user = User()
    user = User()

    @override
    def setUp(self):
        """Create users and client."""
        self.client = Client()
        self.admin_user = create_test_superuser()
        self.client.force_login(self.admin_user)
        self.user = create_test_user()

    def test_users_lists(self):
        """Test that users are listed on page."""
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works."""
        url = reverse("admin:core_user_change", args=[self.user.pk])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works."""
        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

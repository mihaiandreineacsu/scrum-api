"""
Tests for subtask APIs.
"""

from typing import override

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import User
from core.tests.utils import create_test_task, create_test_user, validate_response_data

SUMMARY_URL = reverse("summary:summary")


class PublicSummaryAPITests(TestCase):
    """Test unauthenticated API requests."""

    @override
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(SUMMARY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateSummaryAPITests(TestCase):
    """Test authenticated API requests."""

    user = User()

    @override
    def setUp(self):
        self.user = create_test_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_summary_successful(self):
        _ = create_test_task(user=self.user)
        res = self.client.get(SUMMARY_URL)
        data = validate_response_data(res)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data["tasks_in_lists"]), 1)
        self.assertEqual(len(data["tasks_by_priority"]), 1)
        self.assertEqual(len(data["tasks_by_category"]), 1)

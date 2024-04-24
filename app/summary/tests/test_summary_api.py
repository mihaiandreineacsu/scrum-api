"""
Tests for subtask APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

# from core.models import Summary

# from summary.serializers import (
#     SummarySerializer
# )


SUMMARY_URL = reverse('summary:summary')


def detail_url(summary_id):
    """Create and return a summary detail URL."""
    return reverse('summary:summary-detail', args=[summary_id])


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicSummaryAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(SUMMARY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

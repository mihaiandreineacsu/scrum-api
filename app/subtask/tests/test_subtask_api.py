"""
Tests for task APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Subtask

from subtask.serializers import (
    SubtaskSerializer
)


SUBTASKS_URL = reverse('subtask:subtask-list')


def create_subtask(user, **params):
    """Create and return a sample subtask."""
    defaults = {
        'title': 'Sample task title',
        'done': False
    }
    defaults.update(params)

    subtask = Subtask.objects.create(**defaults)
    return subtask


def detail_url(subtask_id):
    """Create and return a subtask detail URL."""
    return reverse('subtask:subtask-detail', args=[subtask_id])


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicSubtaskAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(SUBTASKS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
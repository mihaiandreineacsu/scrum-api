"""
Tests for board APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Board

from board.serializers import (
    BoardSerializer
)


BOARD_URL = reverse('board:board-list')


def create_board(user, **params):
    """Create and return a sample board."""
    # defaults = {}
    # defaults.update(params)

    # subtask = Board.objects.create(**defaults)
    board = Board.objects.create()
    return board


def detail_url(board_id):
    """Create and return a board detail URL."""
    return reverse('board:board-detail', args=[board_id])


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicSubtaskAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(BOARD_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
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


BOARDS_URL = reverse('board:board-list')


def create_board(user, **params):
    """Create and return a sample board."""
    defaults = {
        'title': 'Some board Title'
    }
    defaults.update(params)

    board = Board.objects.create(user=user,**defaults)
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
        res = self.client.get(BOARDS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBoardAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_boards(self):
        """Test retrieving a board of boards."""
        create_board(user=self.user)
        create_board(user=self.user, title="Other")

        res = self.client.get(BOARDS_URL)

        boards = Board.objects.all().order_by('-id')
        serializer = BoardSerializer(boards, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_board_boards_limited_to_user(self):
        """Test board of boards is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'testpass123',
        )
        create_board(user=other_user)
        create_board(user=self.user, title="My Board")

        res = self.client.get(BOARDS_URL)

        boards = Board.objects.filter(user=self.user).order_by('-id')
        serializer = BoardSerializer(boards, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_board(self):
        """Test creating a board."""
        payload = {
            'title': 'New Board',
        }
        res = self.client.post(BOARDS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        board = Board.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(board, k), v)
        self.assertEqual(board.user, self.user)

    def test_partial_update(self):
        """Test partial update if a board."""
        board = create_board(
            user=self.user,
            title='Board Title',
        )

        payload = {'title': 'Board Title Updated'}
        url = detail_url(board.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        board.refresh_from_db()
        self.assertEqual(board.title, payload['title'])
        self.assertEqual(board.user, self.user)

    def test_full_update(self):
        """Test full update of board."""
        board = create_board(self.user)
        board = create_board(
            user=self.user,
        )

        payload = {
            'title': 'Board full update',
        }
        url = detail_url(board.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        board.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(board, k), v)
        self.assertEqual(board.user, self.user)

    def test_update_user_returns_error(self):
        """test changing the board user results in an error."""
        new_user = create_user(email='user2@example.com', password='test123')
        board = create_board(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(board.id)
        self.client.patch(url, payload)

        board.refresh_from_db()
        self.assertEqual(board.user, self.user)

    def test_deleting_board(self):
        """Test deleting a board successful."""
        board = create_board(user=self.user)

        url = detail_url(board.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Board.objects.filter(id=board.id).exists())

    def test_board_other_users_board_error(self):
        """Test trying to delete another users board gives error."""
        new_user = create_user(email='user2@example.com', password='test123')
        board = create_board(user=new_user)

        url = detail_url(board.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Board.objects.filter(id=board.id).exists())
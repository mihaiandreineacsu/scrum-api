"""
Tests for board APIs.
"""

from typing import override

from django.db.models.query import QuerySet

from board.serializers import BoardSerializer
from core.models import Board
from core.tests.api_test_case import PrivateAPITestCase, PublicAPITestCase
from core.tests.utils import create_test_board


class PublicBoardAPITests(PublicAPITestCase):
    """Test unauthenticated API requests."""

    VIEW_NAME = "board"

    def test_auth_required(self):
        self.assert_auth_required()


class PrivateBoardAPITests(PrivateAPITestCase):
    """Test authenticated API requests."""

    user_board = Board()
    other_user_board = Board()
    api_model = Board
    api_serializer = BoardSerializer

    VIEW_NAME = "board"

    queryset: QuerySet[Board, Board] = Board.objects.all()

    @override
    def setUp(self):
        super().setUp()
        self.user_board = create_test_board(
            user=self.user, title=f"{self.user.name}'s Board"
        )
        self.other_user_board = create_test_board(
            self.other_user, title=f"{self.other_user_board}'s Board"
        )

    def test_create_board(self):
        """Test creating a board."""
        payload = {"title": "New Board", "user": self.other_user.pk}
        self.assert_create_model(payload)

    def test_retrieve_boards(self):
        """Test retrieving boards."""
        self.assert_retrieve_models()

    def test_retrieve_board(self):
        """Test retrieving board."""
        self.assert_retrieve_model(self.user_board.pk)

    def test_partial_update(self):
        """Test partial update a board."""
        payload = {"title": "Boring Board", "user": self.other_user.pk}
        self.assert_update_model(payload, self.user_board, partial_update=True)

    def test_full_update(self):
        """Test full update of board."""
        payload = {"title": "Boring Board", "user": self.other_user.pk}
        self.assert_update_model(payload, self.user_board)

    def test_deleting_board(self):
        """Test deleting a board successful."""
        self.assert_deleting_model(self.user_board)

    def test_deleting_other_user_board_error(self):
        """Test trying to delete another users board gives error."""
        self.assert_deleting_other_user_model_error(self.other_user_board)

    def test_full_updating_other_user_board_error(self):
        """Test trying to put another users board gives error."""
        payload = {"title": "Stolen Board", "user": self.user.pk}
        self.assert_updating_other_user_model_error(payload, self.other_user_board)

    def test_partial_update_other_user_board_error(self):
        """Test trying to patch another users board gives error."""
        payload = {"title": "Stolen Board", "user": self.user.pk}
        self.assert_updating_other_user_model_error(
            payload, self.other_user_board, partial_update=True
        )

    def test_retrieve_other_user_board_error(self):
        """Test trying to retrieve another users board gives error."""
        self.assert_retrieve_other_user_model_error(self.other_user_board.pk)

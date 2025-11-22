"""
Tests for list APIs.
"""

from typing import override

from django.urls import reverse

from core.models import Board, ListOfTasks
from core.tests.api_test_case import (
    PrivateAPITestCase,
    PublicAPITestCase,
)
from core.tests.utils import (
    create_test_board,
    create_test_list_of_tasks,
    validate_response_data,
)
from list_of_tasks.serializers import ListSerializer


class PublicListAPITests(PublicAPITestCase):
    """Test unauthenticated API requests."""

    VIEW_NAME = "list"

    def test_auth_required(self):
        self.assert_auth_required()


class PrivateListAPITests(PrivateAPITestCase):
    """Test authenticated API requests."""

    user_list_of_tasks = ListOfTasks()
    other_user_list_of_tasks = ListOfTasks()
    user_board = Board()
    other_user_board = Board()

    api_model = ListOfTasks
    api_serializer = ListSerializer
    ordering = "-order"
    VIEW_NAME = "list"

    queryset = ListOfTasks.objects.all()

    @override
    def get_queryset(self):
        return self.queryset.filter(board__user=self.user).order_by(self.ordering)

    @override
    def setUp(self) -> None:
        super().setUp()
        self.user_board = create_test_board(self.user)
        self.user_list_of_tasks = create_test_list_of_tasks(
            user=self.user, board=self.user_board
        )

        self.other_user_board = create_test_board(user=self.other_user)
        self.other_user_list_of_tasks = create_test_list_of_tasks(
            user=self.other_user, board=self.other_user_board
        )

    def test_create_list(self):
        """Test creating a list."""
        payload = {
            "name": "DO TODAY",
            "user": self.other_user.pk,
            "board": self.user_board.pk,
        }
        self.assert_create_model(payload)  # TODO: fails issue in view order update

    def test_retrieve_lists(self):
        """Test retrieving lists."""
        self.assert_retrieve_models()

    def test_retrieve_list(self):
        """Test retrieving list."""
        self.assert_retrieve_model(self.user_list_of_tasks.pk)

    def test_partial_update(self):
        """Test partial update a list."""

        updates = [
            {"name": "DO TODAY", "user": self.other_user.pk},
            {"board": self.user_board.pk, "user": self.other_user.pk},
        ]

        for update in updates:
            self.assert_update_model(
                update, self.user_list_of_tasks, partial_update=True
            )

    def test_full_update(self):
        """Test full update of list."""
        payload = {
            "name": "DO TODAY",
            "board": self.user_board.pk,
            "user": self.other_user.pk,
        }
        self.assert_update_model(payload, self.user_list_of_tasks)

    def test_deleting_list(self):
        """Test deleting a list successful."""
        self.assert_deleting_model(self.user_list_of_tasks)

    def test_deleting_other_user_list_error(self):
        """Test trying to delete another users list gives error."""
        self.assert_deleting_other_user_model_error(self.other_user_list_of_tasks)

    def test_full_updating_other_user_list_error(self):
        """Test trying to put another users list gives error."""
        payload = {
            "name": "DO TODAY",
            "board": self.user_board.pk,
            "user": self.user.pk,
        }
        self.assert_updating_other_user_model_error(
            payload, self.other_user_list_of_tasks
        )

    def test_partial_update_other_user_list_error(self):
        """Test trying to patch another users list gives error."""

        updates = [
            {"name": "DO TODAY", "user": self.user.pk},
            {"board": self.user_board.pk, "user": self.user.pk},
        ]

        for update in updates:
            self.assert_updating_other_user_model_error(
                update, self.other_user_list_of_tasks, partial_update=True
            )

    def test_retrieve_other_user_list_error(self):
        """Test trying to retrieve another users list gives error."""
        self.assert_retrieve_other_user_model_error(self.other_user_list_of_tasks.pk)

    def test_move_user_list_order(self):
        """Test move user's list order"""
        in_progess_list = create_test_list_of_tasks(
            user=self.user, board=self.user_board, name="IN PROGRESS"
        )
        next_order = self.user_list_of_tasks.order
        previous_order = in_progess_list.order
        url = reverse("list:list-move", args=[in_progess_list.pk])
        res = self.client.post(url, {"order": next_order})

        data = validate_response_data(res)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["order"], next_order)

        in_progess_list.refresh_from_db()
        self.user_list_of_tasks.refresh_from_db()
        self.assertEqual(in_progess_list.order, next_order)
        self.assertEqual(self.user_list_of_tasks.order, previous_order)

    def test_move_user_list_bad_order(self):
        """Test move user's list bad order"""
        url = reverse("list:list-move", args=[self.user_list_of_tasks.pk])
        res = self.client.post(url, {"order": "bad_order_value"})

        data = validate_response_data(res)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["detail"], "Invalid order")

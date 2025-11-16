"""
Tests for subtask APIs.
"""

# TODO: Test also changing task for a diff user scenario
from typing import override

from core.models import Subtask, Task
from core.tests.api_test_case import PrivateAPITestCase, PublicAPITestCase
from core.tests.utils import (
    create_test_subtask,
    create_test_task,
)
from subtask.serializers import SubtaskSerializer


class PublicSubtaskAPITests(PublicAPITestCase):
    """Test unauthenticated API requests."""

    VIEW_NAME = "subtask"

    def test_auth_required(self):
        self.assert_auth_required()


class PrivateSubtaskAPITests(PrivateAPITestCase):
    """Test authenticated API requests."""

    user_subtask = Subtask()
    user_task = Task()
    other_user_subtask = Subtask()
    other_user_task = Task()

    api_model = Subtask
    api_serializer = SubtaskSerializer
    VIEW_NAME = "subtask"

    queryset = Subtask.objects.all()

    @override
    def get_queryset(self):
        return self.queryset.filter(
            task__list_of_tasks__board__user=self.user
        ).order_by(self.ordering)

    @override
    def setUp(self) -> None:
        super().setUp()
        self.user_task = create_test_task(user=self.user)
        self.user_subtask = create_test_subtask(user=self.user, task=self.user_task)
        self.other_user_task = create_test_task(user=self.other_user)
        self.other_user_subtask = create_test_subtask(
            user=self.other_user, task=self.other_user_task
        )

    def test_create_subtask(self):
        """Test creating a subtask."""
        payload = {
            "title": "New Subtask",
            "done": False,
            "task": self.user_subtask.task.pk,
            "user": self.other_user.pk,
        }
        self.assert_create_model(payload)

    def test_retrieve_subtasks(self):
        """Test retrieving subtasks."""
        self.assert_retrieve_models()

    def test_retrieve_subtask(self):
        """Test retrieving subtask."""
        self.assert_retrieve_model(self.user_subtask.pk)

    def test_partial_update(self):
        """Test partial update a subtask."""

        updates = [
            {"task": self.user_task.pk, "user": self.other_user.pk},  # TODO: is broken
            {
                "title": "Re-Write a unit test for the broken",
                "user": self.other_user.pk,
            },
            {"done": True, "user": self.other_user.pk},
        ]

        for update in updates:
            self.assert_update_model(update, self.user_subtask, partial_update=True)

    def test_full_update(self):
        """Test full update of subtask."""
        payload = {
            "task": self.user_task.pk,
            "title": "Re-Write a unit test for the broken",
            "user": self.other_user.pk,
        }
        self.assert_update_model(payload, self.user_subtask)

    def test_deleting_subtask(self):
        """Test deleting a subtask successful."""
        self.assert_deleting_model(self.user_subtask)

    def test_deleting_other_user_subtask_error(self):
        """Test trying to delete another users subtask gives error."""
        self.assert_deleting_other_user_model_error(self.other_user_subtask)

    def test_full_updating_other_user_subtask_error(self):
        """Test trying to put another users subtask gives error."""
        payload = {
            "title": "Re-Write a unit test for the broken",
            "task": self.user_task.pk,
            "user": self.user.pk,
        }
        self.assert_updating_other_user_model_error(payload, self.other_user_subtask)

    def test_partial_update_other_user_subtask_error(self):
        """Test trying to patch another users subtask gives error."""

        updates = [
            {"title": "Re-Write a unit test for the broken", "user": self.user.pk},
            {"task": self.user_task.pk, "user": self.user.pk},
            {"done": True, "user": self.user.pk},
        ]

        for update in updates:
            self.assert_updating_other_user_model_error(
                update, self.other_user_subtask, partial_update=True
            )

    def test_retrieve_other_user_subtask_error(self):
        """Test trying to retrieve another users subtask gives error."""
        self.assert_retrieve_other_user_model_error(self.other_user_subtask)

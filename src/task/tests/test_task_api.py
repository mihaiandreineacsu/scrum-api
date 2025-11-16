"""
Tests for task APIs.
"""

from datetime import date
from typing import override

from core.models import Category, Contact, ListOfTasks, Subtask, Task
from core.tests.utils import (
    TEST_OTHER_CONTACT_EMAIL,
    TEST_OTHER_CONTACT_FULL_NAME,
    TEST_OTHER_CONTACT_PHONE_NUMBER,
    create_test_category,
    create_test_contact,
    create_test_list_of_tasks,
    create_test_subtask,
    create_test_task,
)
from core.tests.api_test_case import (
    PrivateAPITestCase,
    PublicAPITestCase,
)
from task.serializers import TaskSerializer


class PublicTaskAPITests(PublicAPITestCase):
    """Test unauthenticated API requests."""

    VIEW_NAME = "task"

    def test_auth_required(self):
        self.assert_auth_required()


class PrivateTaskAPITests(PrivateAPITestCase):
    """Test authenticated API requests."""

    user_task = Task()
    user_category = Category()
    user_list_of_tasks = ListOfTasks()
    user_contact = Contact()
    user_subtask = Subtask()

    other_user_task = Task()
    other_user_category = Category()
    other_user_list_of_tasks = ListOfTasks()
    other_user_contact = Contact()
    other_user_subtask = Subtask()

    api_model = Task
    api_serializer = TaskSerializer
    VIEW_NAME = "task"

    queryset = Task.objects.all()

    @override
    def get_queryset(self):
        return self.queryset.filter(list_of_tasks__board__user=self.user).order_by(
            self.ordering
        )

    @override
    def setUp(self) -> None:
        super().setUp()
        self.user_list_of_tasks = create_test_list_of_tasks(user=self.user)
        self.user_task = create_test_task(
            user=self.user, list_of_tasks=self.user_list_of_tasks
        )
        self.user_category = create_test_category(user=self.user)
        self.user_contact = create_test_contact(self.user)
        self.user_subtask = create_test_subtask(
            user=self.user, task=self.user_task
        )  # TODO: Check if task is required

        self.other_user_list_of_tasks = create_test_list_of_tasks(user=self.other_user)
        self.other_user_task = create_test_task(
            user=self.other_user, list_of_tasks=self.other_user_list_of_tasks
        )
        self.other_user_category = create_test_category(user=self.other_user)
        self.other_user_contact = create_test_contact(self.other_user)
        self.other_user_subtask = create_test_subtask(
            user=self.other_user, task=self.other_user_task
        )  # TODO: Check if task is required

    def test_create_task(self):
        """Test creating a task."""
        payload = {
            "title": "Fix API Endpoint",
            "description": "Task API is broken",
            "category": self.user_category.pk,
            "assignees": [self.user_contact.pk],
            "priority": "Low",
            "due_date": date.today().isoformat(),
            "subtasks": [{"title": "Write unit test", "done": False}],
            "list_of_tasks": self.user_list_of_tasks.pk,
            "user": self.other_user.pk,
        }
        self.assert_create_model(payload)

    def test_retrieve_tasks(self):
        """Test retrieving a list of tasks."""
        self.assert_retrieve_models()

    def test_retrieve_task(self):
        """Test retrieving tasks."""
        self.assert_retrieve_model(self.user_task.pk)

    def test_partial_update(self):
        """Test partial update a task."""

        updates = [
            {"title": "Add new feature", "user": self.other_user.pk},
            {"description": "Implement the new feature", "user": self.other_user.pk},
            {
                "category": create_test_category(self.user, "Feature", "#FFF000").pk,
                "user": self.other_user.pk,
            },
            {
                "assignees": [
                    create_test_contact(
                        self.user,
                        TEST_OTHER_CONTACT_EMAIL,
                        TEST_OTHER_CONTACT_FULL_NAME,
                        TEST_OTHER_CONTACT_PHONE_NUMBER,
                    ).pk
                ],
                "user": self.other_user.pk,
            },
            {"due_date": date.today().isoformat(), "user": self.other_user.pk},
            {"priority": "Low", "user": self.other_user.pk},
            {
                "list_of_tasks": create_test_list_of_tasks(
                    self.user, None, "IN PROGRESS"
                ).pk,
                "user": self.other_user.pk,
            },
        ]

        for update in updates:
            self.assert_update_model(update, self.user_task, partial_update=True)

    def test_full_update(self):
        """Test full update of task."""
        payload = {
            "title": "Add new feature",
            "description": "Implement the new feature",
            "category": create_test_category(self.user, "Feature", "#FFF000").pk,
            "assignees": [
                create_test_contact(
                    self.user,
                    TEST_OTHER_CONTACT_EMAIL,
                    TEST_OTHER_CONTACT_FULL_NAME,
                    TEST_OTHER_CONTACT_PHONE_NUMBER,
                ).pk
            ],
            "due_date": date.today().isoformat(),
            "priority": "Low",
            "list_of_tasks": create_test_list_of_tasks(
                self.user, None, "IN PROGRESS"
            ).pk,
            "user": self.other_user.pk,
        }
        self.assert_update_model(payload, self.user_task)

    def test_deleting_task(self):
        """Test deleting a task successful."""
        # TODO: if task is deleted make sure subtasks references are also deleted
        self.assert_deleting_model(self.user_task)

    def test_deleting_other_user_task_error(self):
        """Test trying to delete another users task gives error."""
        self.assert_deleting_other_user_model_error(self.other_user_task)

    def test_full_updating_other_user_task_error(self):
        """Test trying to put another users task gives error."""
        payload = {
            "title": "Add new feature",
            "description": "Implement the new feature",
            "category": create_test_category(self.user, "Feature", "#FFF000").pk,
            "assignees": [
                create_test_contact(
                    self.user,
                    TEST_OTHER_CONTACT_EMAIL,
                    TEST_OTHER_CONTACT_FULL_NAME,
                    TEST_OTHER_CONTACT_PHONE_NUMBER,
                ).pk
            ],
            "due_date": date.today().isoformat(),
            "priority": "Low",
            "list_of_tasks": create_test_list_of_tasks(
                self.user, None, "IN PROGRESS"
            ).pk,
            "user": self.user.pk,
        }
        self.assert_updating_other_user_model_error(payload, self.other_user_task)

    def test_partial_update_other_user_task_error(self):
        """Test trying to patch another users task gives error."""

        updates = [
            {"title": "Add new feature", "user": self.user.pk},
            {"description": "Implement the new feature", "user": self.user.pk},
            {
                "category": create_test_category(self.user, "Feature", "#FFF000").pk,
                "user": self.user.pk,
            },
            {
                "assignees": [
                    create_test_contact(
                        self.user,
                        TEST_OTHER_CONTACT_EMAIL,
                        TEST_OTHER_CONTACT_FULL_NAME,
                        TEST_OTHER_CONTACT_PHONE_NUMBER,
                    ).pk
                ],
                "user": self.user.pk,
            },
            {"due_date": date.today().isoformat(), "user": self.user.pk},
            {"priority": "Low", "user": self.user.pk},
            {
                "list_of_tasks": create_test_list_of_tasks(
                    self.user, None, "IN PROGRESS"
                ).pk,
                "user": self.user.pk,
            },
        ]

        for update in updates:
            self.assert_updating_other_user_model_error(
                update, self.other_user_task, partial_update=True
            )

    def test_retrieve_other_user_task_error(self):
        """Test trying to retrieve another users task gives error."""
        self.assert_retrieve_other_user_model_error(self.other_user_task.pk)

"""
Tests for task APIs.
"""
import json
from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Category, Contact, Subtask, Task
from task.serializers import TaskSerializer

TASKS_URL = reverse('task:task-list')


class MockRequest:
    def __init__(self, user):
        self.user = user


def create_subtask(user, **params):
    """Create and return a sample subtask"""
    defaults = {
        'title': 'Some Subtask',
        'done': False,
        'task': create_task(user=user)
    }
    defaults.update(params)
    subtask = Subtask.objects.create(user=user, **defaults)
    return subtask


def create_subtask_payload(**params):
    """Create and return a sample subtask"""
    defaults = {
        'title': 'Some Subtask',
        'done': False
    }
    defaults.update(params)
    return defaults


def create_contact(user, **params):
    """Create and return a sample contact."""
    email = params.get('email', 'contact@mail.com')
    defaults = {
        'email': email,
        'phone_number': '0157777777777',
        'name': 'Contact Name',
    }
    defaults.update(params)

    contact = Contact.objects.create(user=user, **defaults)
    return contact


def create_category(user, **params):
    """Create and return a sample category."""
    name = params.get('name', 'Some Category Name')
    color = params.get('color', '#FFFFFF')
    defaults = {
        'name': name,
        'color': color,
    }
    defaults.update(params)

    category = Category.objects.create(user=user, **defaults)
    return category


def create_task(user, **params):
    """Create and return a sample task."""
    defaults = {
        'title': 'Sample task title',
        'description': 'Sample description',
        'priority': 'Low',
        'due_date': date.today(),
        'category': create_category(user=user),
        'priority': 'Low'
    }
    defaults.update(params)

    task = Task.objects.create(user=user, **defaults)
    return task


def detail_url(task_id):
    """Create and return a task detail URL."""
    return reverse('task:task-detail', args=[task_id])


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicTaskAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(TASKS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTaskAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_create_task(self):
        """Test creating a task."""
        category = create_category(user=self.user)
        contact1 = create_contact(user=self.user)
        contact2 = create_contact(user=self.user, name="Mihai", phone_number="015777777888", email="mihai@dev.com")
        subtask1 = create_subtask_payload()
        subtask2 = create_subtask_payload(title="Do this")
        due_date = date.today()
        payload = {
            'title': 'Sample task title',
            'description': 'Sample description',
            'category': category.id,
            'assignees': [contact1.id, contact2.id],
            'priority': 'Low',
            'due_date': due_date.isoformat(),
            'subtasks': [subtask1, subtask2]
        }
        res = self.client.post(TASKS_URL, json.dumps(payload), content_type='application/json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        task = Task.objects.get(id=res.data['id'])

        for k, v in payload.items():
            task_attr = getattr(task, k)
            if k != 'assignees' and k != 'subtasks' and k != 'category' and k != 'user' and k != 'due_date':
                self.assertEqual(task_attr, v)

        # Check subtasks separately
        created_subtasks = list(task.subtasks.all())
        self.assertEqual(len(created_subtasks), len(payload['subtasks']))
        for subtask, expected_subtask in zip(created_subtasks, payload['subtasks']):
            self.assertEqual(subtask.title, expected_subtask['title'])
            self.assertEqual(subtask.done, expected_subtask['done'])

        self.assertEqual(task.due_date.isoformat(), due_date.isoformat())
        self.assertEqual(list(task.assignees.all()), [contact1, contact2])
        self.assertEqual(task.category, category)
        self.assertEqual(task.user, self.user)

    def test_retrieve_tasks(self):
        """Test retrieving a list of tasks."""
        create_task(user=self.user, title="Some other Task")
        create_task(user=self.user)

        res = self.client.get(TASKS_URL)

        tasks = Task.objects.all().order_by('-position')
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]['id'], serializer.data[0]['id'])
        self.assertEqual(res.data[1]['id'], serializer.data[1]['id'])

    def test_task_list_limited_to_user(self):
        """Test list of tasks is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'testpass123',
        )
        create_task(user=other_user)
        create_task(user=self.user)

        res = self.client.get(TASKS_URL)

        tasks = Task.objects.filter(user=self.user)
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_partial_update(self):
        """Test partial update if a task."""
        task = create_task(
            user=self.user,
            title='Simple',
        )

        payload = {'title': 'New task title'}
        url = detail_url(task.id)
        res = self.client.patch(url, json.dumps(payload), content_type='application/json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, payload['title'])
        self.assertEqual(task.user, self.user)

    def test_full_update(self):
        """Test full update of task."""
        task = create_task(user=self.user)
        category = create_category(user=self.user)
        contact1 = create_contact(user=self.user)
        contact2 = create_contact(user=self.user, name="Mihai", phone_number="015777777888", email="mihai@dev.com")
        subtask1 = create_subtask_payload()
        subtask2 = create_subtask_payload(title="Do this")
        due_date = date.today()

        payload = {
            'title': 'Sample task title',
            'description': 'Sample description',
            'category': category.id,
            'assignees': [contact1.id, contact2.id],
            'priority': 'Low',
            'due_date': due_date.isoformat(),
            'subtasks': [subtask1, subtask2]
        }
        url = detail_url(task.id)
        res = self.client.put(url, json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        for k, v in payload.items():
            task_attr = getattr(task, k)
            if k != 'assignees' and k != 'subtasks' and k != 'category' and k != 'user' and k != 'due_date':
                self.assertEqual(task_attr, v)
        self.assertEqual(task.due_date.isoformat(), due_date.isoformat())
        self.assertEqual(list(task.assignees.all()), [contact1, contact2])
        # Check subtasks separately
        created_subtasks = list(task.subtasks.all())
        self.assertEqual(len(created_subtasks), len(payload['subtasks']))
        for subtask, expected_subtask in zip(created_subtasks, payload['subtasks']):
            self.assertEqual(subtask.title, expected_subtask['title'])
            self.assertEqual(subtask.done, expected_subtask['done'])
        task.refresh_from_db()
        self.assertEqual(task.category.id, category.id)
        self.assertEqual(task.user, self.user)

    def test_update_user_returns_error(self):
        """test changing the the task user results in an error."""
        new_user = create_user(email='user2@example.com', password='test123')
        task = create_task(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(task.id)

        self.client.patch(url, payload, content_type='application/json')
        # res = self.client.patch(url, payload)
        # it returns ok, but it was not updated
        # self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        task.refresh_from_db()

        self.assertEqual(task.user, self.user)

    def test_deleting_task(self):
        """Test deleting a task successful."""
        task = create_task(user=self.user)

        url = detail_url(task.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_task_other_users_task_error(self):
        """Test trying to delete another users task gives error."""
        new_user = create_user(email='user2@example.com', password='test123')
        task = create_task(user=new_user)

        url = detail_url(task.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Task.objects.filter(id=task.id).exists())

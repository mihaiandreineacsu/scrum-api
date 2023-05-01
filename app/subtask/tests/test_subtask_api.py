"""
Tests for subtask APIs.
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

    subtask = Subtask.objects.create(user=user,**defaults)
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


class PrivateSubtaskAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_subtasks(self):
        """Test retrieving a list of subtasks."""
        create_subtask(user=self.user)
        create_subtask(user=self.user, title="Other")

        res = self.client.get(SUBTASKS_URL)

        subtasks = Subtask.objects.all().order_by('-id')
        serializer = SubtaskSerializer(subtasks, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_subtask_list_limited_to_user(self):
        """Test list of subtasks is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'testpass123',
        )
        create_subtask(user=other_user)
        create_subtask(user=self.user, title="My Subtask")

        res = self.client.get(SUBTASKS_URL)

        subtasks = Subtask.objects.filter(user=self.user).order_by('-id')
        serializer = SubtaskSerializer(subtasks, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_subtask(self):
        """Test creating a subtask."""
        payload = {
            'title': 'New Subtask',
            'done': False,
        }
        res = self.client.post(SUBTASKS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        subtask = Subtask.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(subtask, k), v)
        self.assertEqual(subtask.user, self.user)

    def test_partial_update(self):
        """Test partial update if a subtask."""
        subtask = create_subtask(
            user=self.user,
            title='Subtask Title',
        )

        payload = {'title': 'Subtask Title Updated'}
        url = detail_url(subtask.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        subtask.refresh_from_db()
        self.assertEqual(subtask.title, payload['title'])
        self.assertEqual(subtask.user, self.user)

    def test_full_update(self):
        """Test full update of subtask."""
        subtask = create_subtask(
            user=self.user,
        )

        payload = {
            'title': 'Subtask full update',
            'done': True
        }
        url = detail_url(subtask.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        subtask.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(subtask, k), v)
        self.assertEqual(subtask.user, self.user)

    def test_update_user_returns_error(self):
        """test changing the subtask user results in an error."""
        new_user = create_user(email='user2@example.com', password='test123')
        subtask = create_subtask(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(subtask.id)
        self.client.patch(url, payload)

        subtask.refresh_from_db()
        self.assertEqual(subtask.user, self.user)

    def test_deleting_subtask(self):
        """Test deleting a subtask successful."""
        subtask = create_subtask(user=self.user)

        url = detail_url(subtask.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Subtask.objects.filter(id=subtask.id).exists())

    def test_subtask_other_users_subtask_error(self):
        """Test trying to delete another users subtask gives error."""
        new_user = create_user(email='user2@example.com', password='test123')
        subtask = create_subtask(user=new_user)

        url = detail_url(subtask.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Subtask.objects.filter(id=subtask.id).exists())
"""
Tests for list APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import List, Board

from list.serializers import (
    ListSerializer
)


LISTS_URL = reverse('list:list-list')


def create_board(user):
    """Creates and returns a sample board"""
    board = Board.objects.create(user=user)
    return board


def create_list(user, **params):
    """Create and return a sample list."""
    defaults = {
        'name': 'Some list name'
    }
    defaults.update(params)

    list = List.objects.create(user=user,**defaults)
    return list


def detail_url(list_id):
    """Create and return a list detail URL."""
    return reverse('list:list-detail', args=[list_id])


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicListAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(LISTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateListAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_lists(self):
        """Test retrieving a list of lists."""
        create_list(user=self.user)
        create_list(user=self.user, name="Other")

        res = self.client.get(LISTS_URL)

        lists = List.objects.all().order_by('-id')
        serializer = ListSerializer(lists, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_list_lists_limited_to_user(self):
        """Test list of lists is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'testpass123',
        )
        create_list(user=other_user)
        create_list(user=self.user, name="My List")

        res = self.client.get(LISTS_URL)

        lists = List.objects.filter(user=self.user).order_by('-id')
        serializer = ListSerializer(lists, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_list(self):
        """Test creating a list."""
        payload = {
            'name': 'New List',
        }
        res = self.client.post(LISTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        list = List.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(list, k), v)
        self.assertEqual(list.user, self.user)

    def test_partial_update(self):
        """Test partial update if a list."""
        list = create_list(
            user=self.user,
            name='List Title',
        )

        payload = {'name': 'List Title Updated'}
        url = detail_url(list.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        list.refresh_from_db()
        self.assertEqual(list.name, payload['name'])
        self.assertEqual(list.user, self.user)

    def test_full_update(self):
        """Test full update of list."""
        board = create_board(self.user)
        list = create_list(
            user=self.user,
        )

        payload = {
            'name': 'List full update',
            'board': board.id
        }
        url = detail_url(list.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        list.refresh_from_db()
        for k, v in payload.items():
            if k != 'board':
                self.assertEqual(getattr(list, k), v)
        self.assertEqual(list.board, board)
        self.assertEqual(list.user, self.user)

    def test_update_user_returns_error(self):
        """test changing the list user results in an error."""
        new_user = create_user(email='user2@example.com', password='test123')
        list = create_list(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(list.id)
        self.client.patch(url, payload)

        list.refresh_from_db()
        self.assertEqual(list.user, self.user)

    def test_deleting_list(self):
        """Test deleting a list successful."""
        list = create_list(user=self.user)

        url = detail_url(list.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(List.objects.filter(id=list.id).exists())

    def test_list_other_users_list_error(self):
        """Test trying to delete another users list gives error."""
        new_user = create_user(email='user2@example.com', password='test123')
        list = create_list(user=new_user)

        url = detail_url(list.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(List.objects.filter(id=list.id).exists())
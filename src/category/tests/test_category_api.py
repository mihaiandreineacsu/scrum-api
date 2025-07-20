"""
Tests for category APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Category

from category.serializers import (
    CategorySerializer
)


CATEGORIES_URL = reverse('category:category-list')


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


def detail_url(category_id):
    """Create and return a category detail URL."""
    return reverse('category:category-detail', args=[category_id])


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicCategoryAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(CATEGORIES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCategoryAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_categories(self):
        """Test retrieving a list of categories."""
        create_category(user=self.user)
        create_category(user=self.user, name="Sales", color="#AAABBB")

        res = self.client.get(CATEGORIES_URL)

        categories = Category.objects.all().order_by('name')
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_category_list_limited_to_user(self):
        """Test list of categories is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'testpass123',
        )
        create_category(user=other_user)
        create_category(user=self.user, name="Category 2")

        res = self.client.get(CATEGORIES_URL)

        categories = Category.objects.filter(user=self.user)
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_category(self):
        """Test creating a category."""
        payload = {
            'name': 'Some Category',
            'color': '#000000',
        }
        res = self.client.post(CATEGORIES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        category = Category.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(category, k), v)
        self.assertEqual(category.user, self.user)

    def test_partial_update(self):
        """Test partial update if a category."""
        category = create_category(
            user=self.user,
            color='#AAAAAA',
        )

        payload = {'color': '#BBBBBB'}
        url = detail_url(category.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        category.refresh_from_db()
        self.assertEqual(category.color, payload['color'])
        self.assertEqual(category.user, self.user)

    def test_full_update(self):
        """Test full update of category."""
        category = create_category(
            user=self.user,
        )

        payload = {
            'name': 'Category 2',
            'color': '#CCCCCC',
        }
        url = detail_url(category.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        category.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(category, k), v)
        self.assertEqual(category.user, self.user)

    def test_update_user_returns_error(self):
        """test changing the category user results in an error."""
        new_user = create_user(email='user2@example.com', password='test123')
        category = create_category(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(category.id)
        self.client.patch(url, payload)

        category.refresh_from_db()
        self.assertEqual(category.user, self.user)

    def test_deleting_category(self):
        """Test deleting a category successful."""
        category = create_category(user=self.user)

        url = detail_url(category.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=category.id).exists())

    def test_category_other_users_category_error(self):
        """Test trying to delete another users category gives error."""
        new_user = create_user(email='user2@example.com', password='test123')
        category = create_category(user=new_user)

        url = detail_url(category.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Category.objects.filter(id=category.id).exists())

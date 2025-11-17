"""
Tests for category APIs.
"""

from typing import override

from django.db.models.functions import Lower

from category.serializers import CategorySerializer
from core.models import Category
from core.tests.api_test_case import PrivateAPITestCase, PublicAPITestCase
from core.tests.utils import create_test_category


class PublicCategoryAPITests(PublicAPITestCase):
    """Test unauthenticated API requests."""

    VIEW_NAME = "category"

    def test_auth_required(self):
        self.assert_auth_required()


class PrivateCategoryAPITests(PrivateAPITestCase):
    """Test authenticated API requests."""

    user_category = Category()
    other_user_category = Category()
    api_model = Category
    api_serializer = CategorySerializer
    ordering = Lower("name")
    VIEW_NAME = "category"

    queryset = Category.objects.all()

    @override
    def setUp(self):
        super().setUp()
        self.user_category = create_test_category(user=self.user)
        self.other_user_category = create_test_category(user=self.other_user)

    def test_create_category(self):
        """Test creating a category."""
        payload = {"name": "issue", "color": "#000000", "user": self.other_user.pk}
        self.assert_create_model(payload)

    def test_retrieve_categories(self):
        """Test retrieving a list of categories."""
        self.assert_retrieve_models()

    def test_retrieve_category(self):
        """Test retrieving category."""
        self.assert_deleting_model(self.user_category)

    def test_partial_update(self):
        """Test partial update of a category."""
        updates = [
            {"color": "#BBBBBB", "user": self.user.pk},
            {"name": "feature", "user": self.user.pk},
        ]
        for update in updates:
            self.assert_update_model(update, self.user_category, partial_update=True)

    def test_full_update(self):
        """Test full update of category."""
        payload = {"name": "feature", "color": "#CCCCCC", "user": self.other_user.pk}
        self.assert_update_model(payload, self.user_category)

    def test_deleting_category(self):
        """Test deleting a category successful."""
        self.assert_deleting_model(self.user_category)

    def test_deleting_other_user_category_error(self):
        """Test trying to delete another users category gives error."""
        self.assert_deleting_other_user_model_error(self.other_user_category)

    def test_full_updating_other_user_category_error(self):
        """Test trying to put another users category gives error."""
        payload = {"name": "feature", "color": "#CCCCCC", "user": self.user.pk}
        self.assert_updating_other_user_model_error(payload, self.other_user_category)

    def test_partial_update_other_user_category_error(self):
        """Test trying to patch another users category gives error."""

        updates = [
            {"color": "#BBBBBB", "user": self.user.pk},
            {"name": "feature", "user": self.user.pk},
        ]
        for update in updates:
            self.assert_updating_other_user_model_error(
                update, self.other_user_category, partial_update=True
            )

    def test_retrieve_other_user_category_error(self):
        """Test trying to retrieve another users category gives error."""
        self.assert_retrieve_other_user_model_error(self.other_user_category.pk)

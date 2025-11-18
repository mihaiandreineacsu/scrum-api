"""
Views for the category APIs.
"""

from typing import override

from django.db.models.functions import Lower
from django.db.models.query import QuerySet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import BaseSerializer

from category.serializers import CategorySerializer
from common.serializers_base import CategoryBasedSerializer
from common.views_base import CategoryModelViewSet
from core.models import Category


class CategoryViewSet(CategoryModelViewSet):
    """View for manage category APIs."""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @override
    def get_queryset(self) -> QuerySet[Category]:
        """Retrieve categories for authenticated user."""
        # assert self.queryset is not None
        return self.queryset.filter(user=self.request.user).order_by(Lower("name"))

    @override
    def perform_create(self, serializer: CategoryBasedSerializer):
        """Create a new category."""
        _ = serializer.save(user=self.request.user)

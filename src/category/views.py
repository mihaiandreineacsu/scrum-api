"""
Views for the category APIs.
"""

from typing import override
from django.db.models.functions import Lower
from django.db.models.query import QuerySet
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from category.serializers import CategorySerializer
from core.models import Category


class CategoryViewSet(ModelViewSet[Category]):
    """View for manage category APIs."""

    serializer_class: type[CategorySerializer] = CategorySerializer
    queryset: QuerySet[Category, Category] = Category.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @override
    def get_queryset(self) -> QuerySet[Category, Category]:
        """Retrieve categories for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by(Lower("name"))

    @override
    def get_serializer_class(self) -> type[CategorySerializer]:
        """Return the serializer class for request."""
        if self.action == "list":
            return CategorySerializer

        return self.serializer_class

    @override
    def perform_create(self, serializer: CategorySerializer):
        """Create a new category."""
        _ = serializer.save(user=self.request.user)

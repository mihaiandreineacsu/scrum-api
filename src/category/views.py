"""
Views for the category APIs.
"""

from django.db.models.functions import Lower
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from category import serializers
from core.models import Category


class CategoryViewSet(viewsets.ModelViewSet):
    """View for manage category APIs."""

    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve categories for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by(Lower("name"))

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == "list":
            return serializers.CategorySerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new category."""
        serializer.save(user=self.request.user)

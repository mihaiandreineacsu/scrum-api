"""
Serializers for Category APIs
"""

from rest_framework.serializers import ModelSerializer

from core.models import Category


class CategorySerializer(ModelSerializer):
    """Serializer for categories."""

    class Meta:
        model = Category
        fields = ["id", "name", "color", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

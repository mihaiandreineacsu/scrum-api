"""
Serializers for Category APIs
"""

from typing import TYPE_CHECKING

from rest_framework.serializers import ModelSerializer

from common.serializers_base import CategoryModelSerializer
from core.models import Category


class CategorySerializer(CategoryModelSerializer):
    """Serializer for categories."""

    class Meta:
        model = Category
        fields = ["id", "name", "color", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    if TYPE_CHECKING:
        Meta: type[ModelSerializer.Meta]

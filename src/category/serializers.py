"""
Serializers for Category APIs
"""

from typing import Any
from rest_framework.serializers import ModelSerializer
from rest_framework.utils.serializer_helpers import ReturnDict

from core.models import Category


class CategorySerializer(ModelSerializer[Category]):
    """Serializer for categories."""

    data: ReturnDict[str, Any]

    class Meta:
        model = Category
        fields = ["id", "name", "color", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

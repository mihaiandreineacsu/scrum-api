"""
Serializers for Category APIs
"""

from common.serializers_base import CategoryModelSerializer, ModelSerializerMetaBase
from core.models import Category


class CategorySerializer(CategoryModelSerializer):
    """Serializer for categories."""

    class Meta(ModelSerializerMetaBase):
        model = Category
        fields = ["id", "name", "color", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

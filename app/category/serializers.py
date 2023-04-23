"""
Serializers for Category APIs
"""
from rest_framework import serializers

from core.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for categorys."""

    class Meta:
        model = Category
        fields = ['id', 'name', 'color']
        read_only_fields = ['id',]


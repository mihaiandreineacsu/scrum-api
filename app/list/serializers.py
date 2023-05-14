"""
Serializers for List APIs
"""
from rest_framework import serializers

from core.models import List

class ListSerializer(serializers.ModelSerializer):
    """Serializer for lists."""
    class Meta:
        model = List
        fields = ['id', 'user', 'name', 'board', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

"""
Serializers for Board APIs
"""
from rest_framework import serializers

from core.models import Board


class BoardSerializer(serializers.ModelSerializer):
    """Serializer for boards."""

    class Meta:
        model = Board
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

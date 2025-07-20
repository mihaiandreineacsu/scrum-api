"""
Serializers for Board APIs
"""
from rest_framework import serializers

from core.models import Board
from list.serializers import ListSerializer


class BoardSerializer(serializers.ModelSerializer):
    """Serializer for boards."""
    lists = ListSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'created_at', 'updated_at', 'lists', 'title']
        read_only_fields = ['id', 'created_at', 'updated_at', 'lists']

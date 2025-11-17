"""
Serializers for Board APIs
"""

from rest_framework.serializers import ModelSerializer

from core.models import Board
from list_of_tasks.serializers import ListSerializer


class BoardSerializer(ModelSerializer):
    """Serializer for boards."""

    lists_of_tasks = ListSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ["id", "created_at", "updated_at", "lists_of_tasks", "title"]
        read_only_fields = ["id", "created_at", "updated_at", "lists_of_tasks"]

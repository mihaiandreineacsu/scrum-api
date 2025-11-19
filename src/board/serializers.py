"""
Serializers for Board APIs
"""

from typing import TYPE_CHECKING

from rest_framework.serializers import ModelSerializer

from common.serializers_base import BoardModelSerializer
from core.models import Board
from list_of_tasks.serializers import ListSerializer


class BoardSerializer(BoardModelSerializer):
    """Serializer for boards."""

    lists_of_tasks: ListSerializer = ListSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = [
            "id",
            "created_at",
            "updated_at",
            "lists_of_tasks",
            "title",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "lists_of_tasks",
        ]

    if TYPE_CHECKING:
        Meta: type[ModelSerializer.Meta]

"""
Serializers for ListOfTasks APIs
"""

from typing import Any
from rest_framework.serializers import ModelSerializer
from rest_framework.utils.serializer_helpers import ReturnDict
from core.models import ListOfTasks
from task.serializers import TaskSerializer


class ListSerializer(ModelSerializer[ListOfTasks]):
    """Serializer for lists."""

    tasks = TaskSerializer(many=True, read_only=True)
    data: ReturnDict[str, Any]

    class Meta:
        model = ListOfTasks
        fields = [
            "id",
            "name",
            "board",
            "created_at",
            "updated_at",
            "tasks",
            "order",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "order"]
        write_only_fields = ["board"]

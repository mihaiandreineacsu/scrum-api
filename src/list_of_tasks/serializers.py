"""
Serializers for ListOfTasks APIs
"""

from typing import TYPE_CHECKING

from rest_framework.serializers import IntegerField, ModelSerializer

from common.serializers_base import ListOfTasksModelSerializer
from core.models import ListOfTasks
from task.serializers import TaskSerializer


class ListSerializer(ListOfTasksModelSerializer):
    """Serializer for lists."""

    tasks = TaskSerializer(many=True, read_only=True)
    order = IntegerField(required=False, allow_null=True)

    class Meta:  # pyright: ignore[reportRedeclaration]
        model = ListOfTasks
        fields = ["id", "name", "board", "created_at", "updated_at", "tasks", "order"]
        read_only_fields = ["id", "created_at", "updated_at"]
        write_only_fields = ["board"]

    if TYPE_CHECKING:
        Meta: type[ModelSerializer.Meta]

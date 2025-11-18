"""
Serializers for ListOfTasks APIs
"""

from common.serializers_base import ListOfTasksBasedSerializer, ModelSerializerMetaBase
from core.models import ListOfTasks
from task.serializers import TaskSerializer


class ListSerializer(ListOfTasksBasedSerializer):
    """Serializer for lists."""

    tasks = TaskSerializer(many=True, read_only=True)

    class Meta(ModelSerializerMetaBase):
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

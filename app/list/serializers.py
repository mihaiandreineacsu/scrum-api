"""
Serializers for List APIs
"""
from rest_framework import serializers

from core.models import List
from task.serializers import TaskSerializer


class ListSerializer(serializers.ModelSerializer):
    """Serializer for lists."""

    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = List
        fields = [
            "id",
            "name",
            "board",
            "created_at",
            "updated_at",
            "tasks",
            "position",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
        write_only_fields = ["board"]

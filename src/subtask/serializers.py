"""
Serializers for Subtask APIs
"""

from typing import TYPE_CHECKING, Any

from rest_framework.relations import ManyRelatedField, RelatedField
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from common.serializers_base import SubtaskModelSerializer
from core.models import Subtask, Task


class SubtaskSerializer(SubtaskModelSerializer):
    """Serializer for subtasks which adjusts based on context."""

    task: RelatedField[Task, Task, Any] | ManyRelatedField = PrimaryKeyRelatedField(
        queryset=Task.objects.all()
    )

    class Meta:
        model = Subtask
        fields = ["id", "title", "done", "task", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    if TYPE_CHECKING:
        Meta: type[ModelSerializer.Meta]

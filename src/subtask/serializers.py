"""
Serializers for Subtask APIs
"""

from typing import Any, override

from rest_framework.serializers import PrimaryKeyRelatedField
from common.serializers_base import ModelSerializerMetaBase, SubtaskBasedSerializer
from core.models import Subtask, Task


class SubtaskSerializer(SubtaskBasedSerializer):
    """Serializer for subtasks which adjusts based on context."""

    task = PrimaryKeyRelatedField(queryset=Task.objects.all())

    class Meta(ModelSerializerMetaBase):
        model = Subtask
        fields = ["id", "title", "done", "task", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    @override
    def create(self, validated_data: Any) -> Subtask:
        return super().create(validated_data)

    @override
    def update(self, instance: Subtask, validated_data: Any) -> Subtask:
        return super().update(instance, validated_data)

    @override
    def to_representation(self, instance: Subtask) -> dict[str, Any]:
        representation = super().to_representation(instance)
        return representation

    @override
    def to_internal_value(self, data: dict[str, Any]) -> Task:
        internal_value = super().to_internal_value(data)
        return internal_value

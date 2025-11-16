"""
Serializers for Subtask APIs
"""

from typing import Any, override

from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from rest_framework.utils.serializer_helpers import ReturnDict

from core.models import Subtask, Task


class SubtaskSerializer(ModelSerializer[Subtask]):
    """Serializer for subtasks which adjusts based on context."""

    task = PrimaryKeyRelatedField(queryset=Task.objects.all())
    data: ReturnDict[str, Any]

    class Meta:
        model = Subtask
        fields = ["id", "title", "done", "task", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
        # extra_kwargs = {"task": {"required": False, "queryset": Task.objects.none()}}

    # def __init__(self, *args: Any, **kwargs: Any):
    #     super().__init__(*args, **kwargs)
    #     if self.instance:
    #         # If updating, make 'task' optional
    #         self.fields["task"].required = False
    #     else:
    #         # If creating, ensure 'task' is required
    #         self.fields["task"].required = True

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

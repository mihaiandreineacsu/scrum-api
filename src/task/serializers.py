"""
Serializers for Task APIs
"""

from typing import Any, override

from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from common.serializers_base import ModelSerializerMetaBase, TaskModelSerializer
from category.serializers import CategorySerializer
from contact.serializers import ContactSerializer
from core.models import Category, Contact, ListOfTasks, Subtask, Task
from subtask.serializers import SubtaskSerializer


class TaskSerializer(TaskModelSerializer):
    """Serializer for tasks."""

    subtasks = SubtaskSerializer(many=True, required=False)
    category = PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False,
    )
    assignees = PrimaryKeyRelatedField(
        queryset=Contact.objects.all(), many=True, required=False
    )
    list_of_tasks = PrimaryKeyRelatedField(
        queryset=ListOfTasks.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta(ModelSerializerMetaBase):
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "category",
            "assignees",
            "subtasks",
            "due_date",
            "priority",
            "created_at",
            "updated_at",
            "list_of_tasks",
            "order",
            "order",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]
        ordering = ["order"]

    @override
    def create(self, validated_data: dict[str, Any]) -> Task:
        """TODO: remove order logic from api, forward on model"""
        subtasks_data = validated_data.pop("subtasks", [])

        task = super().create(validated_data)

        _ = Subtask.objects.bulk_create(
            [Subtask(task=task, **sd) for sd in subtasks_data]
        )

        return task

    @override
    def update(self, instance: Task, validated_data: dict[str, Any]) -> Task:
        _ = validated_data.pop("subtasks", [])
        task = super().update(instance, validated_data)

        return task

    @override
    def to_representation(self, instance: Task) -> dict[str, Any]:
        """TODO: use subtask serializer"""
        representation = super().to_representation(instance)
        representation["category"] = (
            CategorySerializer(instance.category).data if instance.category else None
        )
        representation["assignees"] = ContactSerializer(
            instance.assignees.all(), many=True
        ).data
        # self.fields["subtasks"] = SubtaskSerializer(read_only=True, many=True)
        return representation

    @override
    def to_internal_value(self, data: dict[str, Any]) -> Task:
        subtasks = data.pop("subtasks", [])
        internal_value = super().to_internal_value(data)
        internal_value["subtasks"] = subtasks
        return internal_value

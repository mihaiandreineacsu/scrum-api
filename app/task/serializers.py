"""
Serializers for Task APIs
"""
from contact.serializers import ContactSerializer
from rest_framework import serializers

from core.models import Task
from subtask.serializers import SubtaskSerializer


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for tasks."""
    # assignees = ContactSerializer(
    #     many=True,
    #     read_only=True
    # )
    # subtasks = SubtaskSerializer(
    #     many=True,
    #     read_only=True,
    # )
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ('user', 'id')


# class TaskDetailSerializer(TaskSerializer):
#     """Serializer for Task detail view."""

#     class Meta(TaskSerializer.Meta):
#         fields = TaskSerializer.Meta.fields + ['description']

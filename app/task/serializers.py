"""
Serializers for Task APIs
"""
from rest_framework import serializers

from core.models import Task
from category.serializers import CategorySerializer


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for tasks."""
    subtasks = CategorySerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'user', 'assignees', 'subtasks']
        read_only_fields = ['id', 'user']


class TaskDetailSerializer(TaskSerializer):
    """Serializer for Task detail view."""

    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + ['description']

"""
Serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for tasks."""

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'sub_tasks', 'priority']
        read_only_fields = ['id']

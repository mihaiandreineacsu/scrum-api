"""
Serializers for Subtask APIs
"""
from rest_framework import serializers

from core.models import Subtask


class SubtaskSerializer(serializers.ModelSerializer):
    """Serializer for subtasks."""

    class Meta:
        model = Subtask
        fields = ['id', 'title', 'done']
        read_only_fields = ['id']

"""
Serializers for Subtask APIs
"""
from rest_framework import serializers

from core.models import Subtask


class SubtaskSerializer(serializers.ModelSerializer):
    """Serializer for subtasks."""
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Subtask
        fields = ['id', 'title', 'done', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

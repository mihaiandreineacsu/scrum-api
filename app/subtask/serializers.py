"""
Serializers for Subtask APIs
"""
from rest_framework import serializers

from core.models import Subtask

class SubtaskSerializer(serializers.ModelSerializer):
    """Serializer for subtasks."""
    class Meta:
        model = Subtask
        fields = ['id', 'title', 'done','created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

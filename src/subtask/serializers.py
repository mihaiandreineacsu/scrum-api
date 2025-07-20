"""
Serializers for Subtask APIs
"""
from rest_framework import serializers

from core.models import Subtask, Task


class SubtaskSerializer(serializers.ModelSerializer):
    """Serializer for subtasks which adjusts based on context."""
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Subtask
        fields = ['id', 'title', 'done', 'task', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {'task': {'required': False, 'queryset': Task.objects.none()}}

    def __init__(self, *args, **kwargs):
        super(SubtaskSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request', None)
        nested = self.context.get('nested', False)

        if request and not nested:
            # Filter the queryset for task field to include only user's tasks
            self.fields['task'].queryset = Task.objects.filter(user=request.user)
            self.fields['task'].required = True  # Task field required when not nested

        if nested:
            # If nested, do not require the task field
            self.fields['task'].required = False


class SubtaskCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating subtasks with a mandatory task foreign key."""
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())

    class Meta:
        model = Subtask
        fields = ['id', 'title', 'done', 'task', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

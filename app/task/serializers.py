"""
Serializers for Task APIs
"""
from contact.serializers import ContactSerializer
from rest_framework import serializers

from core.models import Task, Contact, Subtask, Category, List
from subtask.serializers import SubtaskSerializer
from category.serializers import CategorySerializer
from user.serializers import UserSerializer


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for tasks."""

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'category', 'assignees', 'subtasks', 'due_date', 'priority', 'created_at', 'updated_at', 'list']
        read_only_fields = ['id', 'created_at', 'updated_at']
        write_only_fields = ['list']

    def to_representation(self, instance):
        self.fields['category'] = CategorySerializer(read_only=True)
        self.fields['assignees'] = ContactSerializer(read_only=True, many=True)
        self.fields['subtasks'] = SubtaskSerializer(read_only=True, many=True)
        return super(TaskSerializer, self).to_representation(instance)

    def to_internal_value(self, data):
        self.fields['category'] = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
        self.fields['assignees'] = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all(), many=True)
        self.fields['subtasks'] = serializers.PrimaryKeyRelatedField(queryset=Subtask.objects.all(), many=True)
        self.fields['list'] = serializers.PrimaryKeyRelatedField(queryset=List.objects.all(), required=False, allow_null=True)
        return super(TaskSerializer, self).to_internal_value(data)

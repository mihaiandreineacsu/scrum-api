"""
Serializers for Task APIs
"""
from contact.serializers import ContactSerializer
from rest_framework import serializers

from core.models import Task, Contact, Subtask, Category
from subtask.serializers import SubtaskSerializer
from category.serializers import CategorySerializer
from user.serializers import UserSerializer


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for tasks."""

    user = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'description', 'category', 'assignees', 'subtasks', 'due_date', 'priority', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def to_representation(self, instance):
        self.fields['category'] = CategorySerializer(read_only=True)
        self.fields['assignees'] = ContactSerializer(read_only=True, many=True)
        self.fields['subtasks'] = SubtaskSerializer(read_only=True, many=True)
        return super(TaskSerializer, self).to_representation(instance)

    def to_internal_value(self, data):
        self.fields['category'] = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
        self.fields['assignees'] = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all(), many=True)
        self.fields['subtasks'] = serializers.PrimaryKeyRelatedField(queryset=Subtask.objects.all(), many=True)
        return super(TaskSerializer, self).to_internal_value(data)

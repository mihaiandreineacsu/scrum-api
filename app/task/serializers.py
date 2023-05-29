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

    subtasks = SubtaskSerializer(many=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'category', 'assignees', 'subtasks', 'due_date', 'priority', 'created_at', 'updated_at', 'list']
        read_only_fields = ['id', 'created_at', 'updated_at']
        write_only_fields = ['list']

    def create(self, validated_data):
        assignees_data = validated_data.pop('assignees', None)
        subtasks_data = validated_data.pop('subtasks', None)
        task = Task.objects.create(**validated_data)
        if assignees_data:
            task.assignees.set(assignees_data)
        if subtasks_data:
            for subtask_data in subtasks_data:
                # You should include the user in the subtask_data
                Subtask.objects.create(task=task, user=task.user, **subtask_data)
        return task

    def to_representation(self, instance):
        self.fields['category'] = CategorySerializer(read_only=True)
        self.fields['assignees'] = ContactSerializer(read_only=True, many=True)
        # self.fields['subtasks'] = SubtaskSerializer(read_only=True, many=True)
        return super(TaskSerializer, self).to_representation(instance)

    def to_internal_value(self, data):
        self.fields['category'] = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
        self.fields['assignees'] = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all(), many=True)
        # self.fields['subtasks'] = serializers.PrimaryKeyRelatedField(queryset=Subtask.objects.all(), many=True)
        self.fields['list'] = serializers.PrimaryKeyRelatedField(queryset=List.objects.all(), required=False, allow_null=True)
        return super(TaskSerializer, self).to_internal_value(data)

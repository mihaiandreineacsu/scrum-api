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
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    assignees = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all(), many=True)
    subtasks = serializers.PrimaryKeyRelatedField(queryset=Subtask.objects.all(), many=True)

    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'description', 'category', 'assignees', 'subtasks', 'due_date', 'priority', 'created_at', 'updated_at']

    def create(self, validated_data):
        assignees_data = validated_data.pop('assignees', [])
        subtasks_data = validated_data.pop('subtasks', [])
        category_data = validated_data.pop('category', None)
        task = Task.objects.create(**validated_data)
        task.assignees.set(assignees_data)
        task.subtasks.set(subtasks_data)
        task.category = Category.objects.get(id=category_data.id) if category_data else None
        task.save()
        return task

    def update(self, instance, validated_data):
        assignees_data = validated_data.pop('assignees', [])
        subtasks_data = validated_data.pop('subtasks', [])
        category_data = validated_data.pop('category', None)

        # Update simple fields
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.save()

        # Update category
        instance.category = Category.objects.get(id=category_data.id) if category_data else None

        # Update assignees
        instance.assignees.set(assignees_data)

        # Update subtasks
        instance.subtasks.set(subtasks_data)

        instance.save()
        return instance


# class TaskDetailSerializer(TaskSerializer):
#     """Serializer for Task detail view."""

#     class Meta(TaskSerializer.Meta):
#         fields = TaskSerializer.Meta.fields + ['description']

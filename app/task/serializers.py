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

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        # ... any other fields you want to update directly on the Task

        # Update related Subtasks
        subtasks_data = validated_data.pop('subtasks', None)
        if subtasks_data is not None:
            for subtask_data in subtasks_data:
                subtask_id = subtask_data.get('id', None)
                if subtask_id:
                    # If the subtask already exists, update it
                    subtask = instance.subtasks.get(id=subtask_id)
                    for attr, value in subtask_data.items():
                        setattr(subtask, attr, value)
                    subtask.save()
                else:
                    # If the subtask does not exist, create it
                    Subtask.objects.create(user=instance.user, task=instance, **subtask_data)

        instance.save()
        return instance

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

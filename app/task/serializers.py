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
        fields = ['id', 'title', 'description', 'category', 'assignees', 'subtasks', 'due_date', 'priority', 'created_at', 'updated_at', 'list', 'order']
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
        instance.category = validated_data.get('category', instance.category)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.list = validated_data.get('list', instance.list)
        assignees_data = validated_data.pop('assignees', None)
        subtasks_data = validated_data.pop('subtasks', None)

        if assignees_data:
            instance.assignees.set(assignees_data)
        # ... any other fields you want to update directly on the Task

        # Update related Subtasks

        if subtasks_data is not None:
            if len(subtasks_data) == 0:
                instance.subtasks.all().delete()
            else:
                for subtask_data in subtasks_data:
                    subtask_id = subtask_data.get('id', None)
                    if subtask_id:
                        try:
                            subtask = instance.subtasks.get(id=subtask_id)
                            for attr, value in subtask_data.items():
                                setattr(subtask, attr, value)
                            subtask.save()
                        except Subtask.DoesNotExist:
                            raise serializers.ValidationError("Subtask with id %s does not exist" % subtask_id)
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

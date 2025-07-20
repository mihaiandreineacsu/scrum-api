"""
Serializers for Task APIs
"""
from rest_framework import serializers

from category.serializers import CategorySerializer
from contact.serializers import ContactSerializer
from core.models import Category, Contact, List, Subtask, Task
from subtask.serializers import SubtaskSerializer


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for tasks."""

    subtasks = SubtaskSerializer(many=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "category",
            "assignees",
            "subtasks",
            "due_date",
            "priority",
            "created_at",
            "updated_at",
            "list",
            "order",
            "position",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
        write_only_fields = ["list"]
        ordering = ["position"]

    def create(self, validated_data):
        assignees_data = validated_data.pop("assignees", None)
        subtasks_data = validated_data.pop("subtasks", None)
        task = Task.objects.create(**validated_data)
        if assignees_data:
            task.assignees.set(assignees_data)
        if subtasks_data:
            for subtask_data in subtasks_data:
                # You should include the user in the subtask_data
                Subtask.objects.create(task=task, user=task.user, **subtask_data)
        return task

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.category = validated_data.get("category", instance.category)
        instance.due_date = validated_data.get("due_date", instance.due_date)
        instance.priority = validated_data.get("priority", instance.priority)
        instance.list = validated_data.get("list", instance.list)

        assignees_data = validated_data.pop("assignees", None)
        subtasks_data = validated_data.pop("subtasks", None)

        if assignees_data is not None:
            instance.assignees.set(assignees_data)

        self.update_subtasks(instance, subtasks_data)

        instance.save()
        return instance

    def update_subtasks(self, instance, subtasks_data):
        if subtasks_data is None:
            return

        subtask_ids = {data.get('id') for data in subtasks_data if data.get('id') is not None}
        existing_subtasks = {subtask.id: subtask for subtask in instance.subtasks.all()}

        # Delete subtasks not included in the update
        subtasks_to_delete = existing_subtasks.keys() - subtask_ids
        if subtasks_to_delete:
            instance.subtasks.filter(id__in=subtasks_to_delete).delete()

        # Update existing subtasks and create new ones
        for subtask_data in subtasks_data:
            subtask_id = subtask_data.get("id", None)
            if subtask_id and subtask_id in existing_subtasks:
                subtask = existing_subtasks[subtask_id]
                for attr, value in subtask_data.items():
                    setattr(subtask, attr, value)
                subtask.save()
            elif not subtask_id:
                Subtask.objects.create(user=instance.user, task=instance, **subtask_data)

    def to_representation(self, instance):
        self.fields["category"] = CategorySerializer(read_only=True)
        self.fields["assignees"] = ContactSerializer(read_only=True, many=True)
        # self.fields['subtasks'] = SubtaskSerializer(read_only=True, many=True)
        return super(TaskSerializer, self).to_representation(instance)

    def to_internal_value(self, data):
        self.fields["category"] = serializers.PrimaryKeyRelatedField(
            queryset=Category.objects.all()
        )
        self.fields["assignees"] = serializers.PrimaryKeyRelatedField(
            queryset=Contact.objects.all(), many=True
        )
        # self.fields['subtasks'] = serializers.PrimaryKeyRelatedField(queryset=Subtask.objects.all(), many=True)
        self.fields["list"] = serializers.PrimaryKeyRelatedField(
            queryset=List.objects.all(), required=False, allow_null=True
        )
        return super(TaskSerializer, self).to_internal_value(data)

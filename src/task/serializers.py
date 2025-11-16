"""
Serializers for Task APIs
"""

from typing import Any, override

from django.db.models import Max

from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from category.serializers import CategorySerializer
from contact.serializers import ContactSerializer
from core.models import Category, Contact, ListOfTasks, Subtask, Task
from subtask.serializers import SubtaskSerializer


class TaskSerializer(ModelSerializer[Task]):
    """Serializer for tasks."""

    subtasks = SubtaskSerializer(many=True, required=False)
    category = PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False,
    )
    assignees = PrimaryKeyRelatedField(
        queryset=Contact.objects.all(), many=True, required=False
    )
    list_of_tasks = PrimaryKeyRelatedField(
        queryset=ListOfTasks.objects.all(),
        required=False,
        allow_null=True,
    )

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
            "list_of_tasks",
            "order",
            "order",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]
        ordering = ["order"]

    @override
    def create(self, validated_data: dict[str, Any]) -> Task:
        """TODO: remove order logic from api, forward on model"""
        subtasks_data = validated_data.pop("subtasks", [])
        # list_data = validated_data.get(
        #     "list_of_tasks", None
        # )  # TODO: can be used to access list of other user?
        # max_position = Task.objects.filter(list_of_tasks=list_data).aggregate(
        #     Max("order")
        # )["order__max"]
        # validated_data.update({"order": (max_position or 0) + 1})

        task = super().create(validated_data)

        _ = Subtask.objects.bulk_create(
            [Subtask(task=task, **sd) for sd in subtasks_data]
        )

        return task

    @override
    def update(self, instance: Task, validated_data: dict[str, Any]) -> Task:
        _ = validated_data.pop("subtasks", [])
        task = super().update(instance, validated_data)

        return task
        # category_data = validated_data.pop("category", None)
        # if category_data:
        #     instance.category = Category.objects.get(id=category_data["id"])

        # assignees_data = validated_data.pop("assignees", [])
        # if assignees_data:
        #     instance.assignees.set(
        #         [Contact.objects.get(id=assignee["id"]) for assignee in assignees_data]
        #     )

        # list_data = validated_data.pop("list")
        # if list_data:
        #     instance.list = ListOfTasks.objects.get(id=list_data)

        # Subtasks are not processed in update
        # _ = validated_data.pop("subtasks", None)

        # for attr, value in validated_data.items():
        #     setattr(instance, attr, value)
        # instance.save()
        # return instance

    # def update_subtasks(
    #     self, instance: Task, subtasks_data: list[dict[str, Any]] | None
    # ):
    #     if subtasks_data is None:
    #         return

    #     subtask_ids = {
    #         data.get("id") for data in subtasks_data if data.get("id") is not None
    #     }
    #     existing_subtasks = {subtask.id: subtask for subtask in instance.subtasks.all()}

    #     # Delete subtasks not included in the update
    #     subtasks_to_delete = existing_subtasks.keys() - subtask_ids
    #     if subtasks_to_delete:
    #         instance.subtasks.filter(id__in=subtasks_to_delete).delete()

    #     # Update existing subtasks and create new ones
    #     for subtask_data in subtasks_data:
    #         subtask_id = subtask_data.get("id", None)
    #         if subtask_id and subtask_id in existing_subtasks:
    #             subtask: Subtask = existing_subtasks[subtask_id]
    #             for attr, value in subtask_data.items():
    #                 setattr(subtask, attr, value)
    #             subtask.save()
    #         elif not subtask_id:
    #             _ = Subtask.objects.create(
    #                 user=instance.user, task=instance, **subtask_data
    #             )

    @override
    def to_representation(self, instance: Task) -> dict[str, Any]:
        """TODO: use subtask serializer"""
        representation = super().to_representation(instance)
        representation["category"] = (
            CategorySerializer(instance.category).data if instance.category else None
        )
        representation["assignees"] = ContactSerializer(
            instance.assignees.all(), many=True
        ).data
        # self.fields["subtasks"] = SubtaskSerializer(read_only=True, many=True)
        return representation

    @override
    def to_internal_value(self, data: dict[str, Any]) -> Task:
        subtasks = data.pop("subtasks", [])
        internal_value = super().to_internal_value(data)
        internal_value["subtasks"] = subtasks
        return internal_value

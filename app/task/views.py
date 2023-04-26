"""
Views for the task APIs.
"""
import json
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Task, Subtask
from task import serializers


class TaskViewSet(viewsets.ModelViewSet):
    """View for manage task APIs."""
    serializer_class = serializers.TaskSerializer
    queryset = Task.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve tasks for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.TaskSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new task."""
        # subtasks_data = self.request.data.get('subtasks', [])
        # if isinstance(subtasks_data, str):
        #     subtasks_data = json.loads(subtasks_data)
        # assignees_data = self.request.data.get('assignees', [])

        task = serializer.save(user=self.request.user)
        # task.assignees.set(assignees_data)

        # subtasks = []
        # for subtask_data in subtasks_data:
        #     subtask = Subtask(task=task,user=self.request.user,**subtask_data)
        #     subtasks.append(subtask)

        # if subtasks:
        #     Subtask.objects.bulk_create(subtasks)

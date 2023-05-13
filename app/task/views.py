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
        task = serializer.save(user=self.request.user)

"""
Views for the task APIs.
"""
import json
from rest_framework import viewsets, filters
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
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        """Retrieve tasks for authenticated user."""
        queryset = self.queryset.filter(user=self.request.user).order_by('-id')
        # Get the query parameter
        list_is_null = self.request.query_params.get('list_is_null', None)

        if list_is_null is not None:
            queryset = queryset.filter(list__isnull=list_is_null.lower() in ['true', '1', 'yes'])

        return queryset

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.TaskSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new task."""
        task = serializer.save(user=self.request.user)

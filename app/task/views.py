"""
Views for the task APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Task
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

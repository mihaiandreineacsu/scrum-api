"""
Views for the subtask APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Subtask
from subtask import serializers


class SubtaskViewSet(viewsets.ModelViewSet):
    """View for manage subtask APIs."""
    serializer_class = serializers.SubtaskSerializer
    queryset = Subtask.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     """Retrieve tasks for authenticated user."""
    #     return self.queryset.filter(user=self.request.user).order_by('-id')

    # def get_serializer_class(self):
    #     """Return the serializer class for request."""
    #     if self.action == 'list':
    #         return serializers.TaskSerializer

    #     return self.serializer_class

    # def perform_create(self, serializer):
    #     """Create a new task."""
    #     serializer.save(user=self.request.user)

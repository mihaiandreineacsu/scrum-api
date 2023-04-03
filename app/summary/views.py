"""
Views for the summary APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Summary
from summary import serializers


class SummaryViewSet(viewsets.ModelViewSet):
    """View for manage summary APIs."""
    serializer_class = serializers.SummarySerializer
    queryset = Summary.objects.all()
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

"""
Views for the list APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import List
from list import serializers


class ListViewSet(viewsets.ModelViewSet):
    """View for manage list APIs."""
    serializer_class = serializers.ListSerializer
    queryset = List.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve list for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.ListSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new list."""
        serializer.save(user=self.request.user)

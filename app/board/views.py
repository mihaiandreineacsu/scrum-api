"""
Views for the board APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Board
from board import serializers


class BoardViewSet(viewsets.ModelViewSet):
    """View for manage board APIs."""
    serializer_class = serializers.BoardSerializer
    queryset = Board.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve boards for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.BoardSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new board."""
        serializer.save(user=self.request.user)

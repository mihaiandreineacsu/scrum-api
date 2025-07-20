"""
Views for the board APIs.
"""

from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from board import serializers
from core.models import Board, List, Task


class BoardViewSet(viewsets.ModelViewSet):
    """View for manage board APIs."""

    serializer_class = serializers.BoardSerializer
    queryset = Board.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve boards for authenticated user with lists and tasks ordered by position."""
        return (
            self.queryset.filter(user=self.request.user)
            .prefetch_related(
                Prefetch(
                    "lists",
                    queryset=List.objects.prefetch_related(
                        Prefetch("tasks", queryset=Task.objects.order_by("-position"))
                    ).order_by("-position"),
                )
            )
            .order_by("-id")
        )

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == "list":
            return serializers.BoardSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new board."""
        serializer.save(user=self.request.user)

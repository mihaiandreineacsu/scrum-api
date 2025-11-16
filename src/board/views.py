"""
Views for the board APIs.
"""

from typing import override

from django.db.models import Prefetch
from django.db.models.query import QuerySet
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from board.serializers import BoardSerializer
from core.models import Board, ListOfTasks, Task


class BoardViewSet(ModelViewSet[Board]):
    """View for manage board APIs."""

    serializer_class: type[BoardSerializer] = BoardSerializer
    queryset: QuerySet[Board, Board] = Board.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @override
    def get_queryset(self) -> QuerySet[Board, Board]:
        """
        Retrieve boards for authenticated user
        with lists_of_tasks and tasks ordered by order.
        """
        # TODO: Is this covered by tests?
        return (
            self.queryset.filter(user=self.request.user)
            .prefetch_related(
                Prefetch(
                    "lists_of_tasks",
                    queryset=ListOfTasks.objects.prefetch_related(
                        Prefetch("tasks", queryset=Task.objects.order_by("-order"))
                    ).order_by("-order"),
                )
            )
            .order_by("-id")
        )

    @override
    def get_serializer_class(self) -> type[BoardSerializer]:
        """Return the serializer class for request."""
        if self.action == "list":
            return BoardSerializer

        return self.serializer_class

    @override
    def perform_create(self, serializer: BoardSerializer):
        """Create a new board."""
        _ = serializer.save(user=self.request.user)

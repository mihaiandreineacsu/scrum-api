"""
Views for the board APIs.
"""

from typing import override

from django.db.models import Prefetch
from django.db.models.query import QuerySet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from board.serializers import BoardSerializer
from common.serializers_base import BoardBasedSerializer
from common.views_base import BoardModelViewSet
from core.models import Board, ListOfTasks, Task


class BoardViewSet(BoardModelViewSet):
    """View for manage board APIs."""

    serializer_class = BoardSerializer
    queryset = Board.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @override
    def get_queryset(self) -> QuerySet[Board]:
        """
        Retrieve boards for authenticated user
        with lists_of_tasks and tasks ordered by order.
        """
        assert self.queryset is not None
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
    def perform_create(self, serializer: BoardBasedSerializer):
        """Create a new board."""
        _ = serializer.save(user=self.request.user)

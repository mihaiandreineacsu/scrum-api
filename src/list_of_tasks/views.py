"""
Views for the list APIs.
"""

from typing import override

from django.db.models import Prefetch
from django.db.models.query import QuerySet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from common.serializers_base import ListOfTasksBasedSerializer
from common.views_base import ListOfTasksModelViewSet
from core.models import ListOfTasks, Task
from list_of_tasks.serializers import ListSerializer


class ListViewSet(ListOfTasksModelViewSet):
    """View for manage list APIs."""

    serializer_class = ListSerializer
    queryset = ListOfTasks.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @override
    def get_queryset(self) -> QuerySet[ListOfTasks]:
        """Retrieve list for authenticated user."""
        # Prefetch related tasks to optimize query performance
        assert self.queryset is not None
        return (
            self.queryset.filter(board__user=self.request.user)
            .prefetch_related(
                Prefetch("tasks", queryset=Task.objects.order_by("-order"))
            )
            .order_by("-id")
        )

    @override
    def perform_create(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, serializer: ListOfTasksBasedSerializer
    ):
        """Create a new list."""
        _ = serializer.save(user=self.request.user)

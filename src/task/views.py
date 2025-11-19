"""
Views for the task APIs.
"""

from typing import override

from django.db.models import Prefetch
from django.db.models.query import QuerySet
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from common.serializers_base import TaskBasedSerializer
from common.views_base import TaskModelViewSet
from core.models import Subtask, Task
from task.serializers import TaskSerializer


class TaskViewSet(TaskModelViewSet):
    """View for manage task APIs."""

    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]

    @override
    def get_queryset(self) -> QuerySet[Task]:
        """Retrieve tasks for authenticated user."""
        assert self.queryset is not None
        queryset = (
            self.queryset.filter(list_of_tasks__board__user=self.request.user)
            .order_by("-order")
            .prefetch_related(
                Prefetch("subtasks", queryset=Subtask.objects.order_by("-id"))
            )
        )

        return queryset

    @override
    def perform_create(self, serializer: TaskBasedSerializer):
        """Create a new task."""
        _ = serializer.save(user=self.request.user)

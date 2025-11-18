"""
Views for the list APIs.
"""

from typing import Any, override

from django.db.models import Prefetch
from django.db.models.query import QuerySet
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

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

    @action(detail=True, methods=["post"])
    def move(self, request: Request, pk: Any = None):
        list_of_tasks = self.get_object()
        order = request.data.get("order") or ""
        assert str(order).isdigit(), "Order must be an integer"

        try:
            order = int(order)
        except (TypeError, ValueError):
            return Response({"error": "Invalid order"})

        list_of_tasks.to(order)
        list_of_tasks.save()

        return Response(ListSerializer(list_of_tasks).data)

    @override
    def perform_create(self, serializer: ListOfTasksBasedSerializer):
        """Create a new list."""
        _ = serializer.save(user=self.request.user)

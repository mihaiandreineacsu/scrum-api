"""
Views for the list APIs.
"""

from typing import Any, override
from django.db.models import Prefetch
from django.db.models.query import QuerySet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from core.models import ListOfTasks, Task
from list_of_tasks.serializers import ListSerializer


class ListViewSet(ModelViewSet[ListOfTasks]):
    """View for manage list APIs."""

    serializer_class: type[ListSerializer] = ListSerializer
    queryset: QuerySet[ListOfTasks, ListOfTasks] = ListOfTasks.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @override
    def get_queryset(self) -> QuerySet[ListOfTasks, ListOfTasks]:
        """Retrieve list for authenticated user."""
        # Prefetch related tasks to optimize query performance
        return (
            self.queryset.filter(board__user=self.request.user)
            .prefetch_related(
                Prefetch("tasks", queryset=Task.objects.order_by("-order"))
            )
            .order_by("-id")
        )

    @override
    def get_serializer_class(self) -> type[ListSerializer]:
        """Return the serializer class for request."""
        if self.action == "list":
            return ListSerializer

        return self.serializer_class

    @action(detail=True, methods=["post"])
    def move(self, request: Request, pk: Any = None):
        list_of_tasks = self.get_object()
        order = request.data.get("order")

        try:
            order = int(order)
        except (TypeError, ValueError):
            return Response({"error": "Invalid order"})

        list_of_tasks.to(order)
        list_of_tasks.save()

        return Response(ListSerializer(list_of_tasks).data)

    # @override
    # def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
    #     board = request.data.get("board")
    #     max_position = ListOfTasks.objects.filter(board=board).aggregate(
    #         Max("order")
    #     )["position__max"]
    #     request.data.update({"order": (max_position or 0) + 1})
    #     return super().create(request, *args, **kwargs)

    # @override
    # def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
    #     try:
    #         return super().update(request, *args, **kwargs)
    #     except PositionException as e:
    #         return Response(
    #             data={"message": str(e), "status": e.status_code, "error": str(e.error)}
    #         )

    @override
    def perform_create(self, serializer: ListSerializer):
        """Create a new list."""
        _ = serializer.save(user=self.request.user)

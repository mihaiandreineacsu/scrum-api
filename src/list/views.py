"""
Views for the list APIs.
"""

from django.db.models import Max, Prefetch
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import List, Task
from list import serializers
from position.position_exception import PositionException
from position.views import PositionViewSet


class ListViewSet(PositionViewSet):
    """View for manage list APIs."""

    serializer_class = serializers.ListSerializer
    queryset = List.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve list for authenticated user."""
        # Prefetch related tasks to optimize query performance
        return (
            self.queryset.filter(user=self.request.user)
            .prefetch_related(
                Prefetch("tasks", queryset=Task.objects.order_by("-position"))
            )
            .order_by("-id")
        )

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == "list":
            return serializers.ListSerializer

        return self.serializer_class

    def create(self, request, **args):
        board = request.data.get("board")
        max_position = List.objects.filter(board=board).aggregate(Max("position"))[
            "position__max"
        ]
        request.data.update({"position": (max_position or 0) + 1})
        return super().create(request, *args)

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except PositionException as e:
            return Response(
                data={"message": str(e), "status": e.status_code, "error": str(e.error)}
            )

    def perform_create(self, serializer):
        """Create a new list."""
        serializer.save(user=self.request.user)

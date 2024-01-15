"""
Views for the task APIs.
"""
from position.views import PositionViewSet
from position.position_exception import PositionException
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Task
from task import serializers
from django.db.models import Max


class TaskViewSet(PositionViewSet):
    """View for manage task APIs."""

    serializer_class = serializers.TaskSerializer
    queryset = Task.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        """Retrieve tasks for authenticated user."""
        queryset = self.queryset.filter(user=self.request.user).order_by("-position")
        # Get the query parameter
        list_is_null = self.request.query_params.get("list_is_null", None)

        if list_is_null is not None:
            queryset = queryset.filter(
                list__isnull=list_is_null.lower() in ["true", "1", "yes"]
            )

        return queryset

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == "list":
            return serializers.TaskSerializer

        return self.serializer_class

    def create(self, request, **args):
        new_list = request.data.get("list")
        max_position = Task.objects.filter(list=new_list).aggregate(Max("position"))[
            "position__max"
        ]
        request.data.update({"position": (max_position or 0) + 1})
        return super().create(request, *args)

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except PositionException as e:
            return Response(data={"message": str(e), "status": e.status_code, "error": str(e.error)})

    def perform_create(self, serializer):
        """Create a new task."""
        # task = serializer.save(user=self.request.user)
        serializer.save(user=self.request.user)

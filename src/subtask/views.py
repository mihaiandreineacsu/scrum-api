"""
Views for the subtask APIs.
"""

from typing import override

from django.db.models.query import QuerySet
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Subtask
from subtask.serializers import SubtaskSerializer


class SubtaskViewSet(ModelViewSet[Subtask]):
    """View for manage subtask APIs."""

    serializer_class: type[SubtaskSerializer] = SubtaskSerializer
    queryset: QuerySet[Subtask, Subtask] = Subtask.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @override
    def get_queryset(self) -> QuerySet[Subtask, Subtask]:
        """Retrieve tasks for authenticated user."""
        return self.queryset.filter(
            task__list_of_tasks__board__user=self.request.user
        ).order_by("-id")

    @override
    def get_serializer_class(self) -> type[SubtaskSerializer]:
        """Return the serializer class for request."""
        if self.action == "list":
            return SubtaskSerializer

        return self.serializer_class

    @override
    def perform_create(self, serializer: SubtaskSerializer):
        """Create a new subtask."""
        _ = serializer.save(user=self.request.user)

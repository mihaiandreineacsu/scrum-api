"""
Views for the subtask APIs.
"""

from typing import override

from django.db.models.query import QuerySet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet

from common.serializers_base import SubtaskBasedSerializer
from common.views_base import SubtaskModelViewSet
from core.models import Subtask
from subtask.serializers import SubtaskSerializer


class SubtaskViewSet(SubtaskModelViewSet):
    """View for manage subtask APIs."""

    serializer_class = SubtaskSerializer
    queryset = Subtask.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @override
    def get_queryset(self) -> QuerySet[Subtask]:
        """Retrieve tasks for authenticated user."""
        assert self.queryset is not None
        return self.queryset.filter(
            task__list_of_tasks__board__user=self.request.user
        ).order_by("-id")

    @override
    def perform_create(self, serializer: SubtaskBasedSerializer):
        """Create a new subtask."""
        _ = serializer.save(user=self.request.user)

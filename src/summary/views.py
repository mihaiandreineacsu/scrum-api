"""
Views for the summary APIs.
"""

from django.db.models import Count, Max
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Task


class SummaryView(APIView):
    """View for manage summary APIs."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        """Retrieve summary for authenticated user."""
        user = request.user
        user_tasks = Task.objects.filter(list_of_tasks__board__user=user)

        tasks_in_lists = (
            user_tasks.values(
                "list_of_tasks__board__title",
                "list_of_tasks__name",
                "list_of_tasks__order",
            )
            .annotate(count=Count("id"), latest_due_date=Max("due_date"))
            .order_by(
                "list_of_tasks__board__title",
                "list_of_tasks__order",
            )
        )

        # Count tasks for each priority and get the latest due date for each
        tasks_by_priority = (
            user_tasks.values("priority")
            .annotate(count=Count("id"), latest_due_date=Max("due_date"))
            .order_by("priority")
        )

        # Count tasks for each category and get the latest due date for each
        tasks_by_category = (
            user_tasks.values("category__name", "category__color")
            .annotate(count=Count("id"), latest_due_date=Max("due_date"))
            .order_by("category__name")
        )

        # Construct response
        return Response(
            {
                "tasks_in_lists": list(tasks_in_lists),
                "tasks_by_priority": list(tasks_by_priority),
                "tasks_by_category": list(tasks_by_category),
            }
        )

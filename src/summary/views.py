"""
Views for the summary APIs.
"""

from django.db.models import Count, Max
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Task, User


class SummaryView(APIView):
    """View for manage summary APIs."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        """Retrieve summary for authenticated user."""
        user: User = request.user
        # Count tasks in each list and include list names and positions and get the latest due date for each
        tasks_in_lists = (
            Task.objects.filter(user=user)
            .exclude(list__isnull=True)
            .values("list__board__title", "list__name", "list__position")
            .annotate(count=Count("id"), latest_due_date=Max("due_date"))
            .order_by("list__board__title", "list__position")
        )

        # Count tasks for each priority and get the latest due date for each
        tasks_by_priority = (
            Task.objects.filter(user=user)
            .values("priority")
            .annotate(count=Count("id"), latest_due_date=Max("due_date"))
            .order_by("priority")
        )

        # Count tasks for each category and get the latest due date for each
        tasks_by_category = (
            Task.objects.filter(user=user)
            .values("category__name", "category__color")
            .annotate(count=Count("id"), latest_due_date=Max("due_date"))
            .order_by("category__name")
        )

        # Modify the tasks_in_backlog query to include latest_due_date
        tasks_in_backlog = Task.objects.filter(user=user, list__isnull=True).aggregate(
            count=Count("id"), latest_due_date=Max("due_date")
        )
        # Upcoming deadline Task
        # most_recent_deadline = Task.objects.filter(user=user).order_by('-due_date').first()

        # Construct response
        return Response(
            {
                "tasks_in_lists": list(
                    tasks_in_lists
                ),  # Convert to list for JSON serialization
                "tasks_by_priority": list(tasks_by_priority),
                "tasks_in_backlog": tasks_in_backlog,
                "tasks_by_category": list(tasks_by_category),
                # 'most_recent_deadline': most_recent_deadline TODO throws error
            }
        )

"""
Views for the summary APIs.
"""
from django.db.models import Count, Max
from core.models import Task
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class SummaryView(APIView):
    """View for manage summary APIs."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """Retrieve summary for authenticated user."""
        user = request.user
        # Count tasks in each list and include list names and positions
        tasks_in_lists = Task.objects.filter(user=user).exclude(list__isnull=True) \
            .values('list__board__title', 'list__name', 'list__position') \
            .annotate(count=Count('id')) \
            .order_by('list__board__title', 'list__position') # Adjust ordering as needed

        # Count tasks for each priority and get the latest due date for each
        tasks_by_priority = Task.objects.filter(user=user).values('priority').annotate(
            count=Count('id'),
            latest_due_date=Max('due_date')
        ).order_by('priority')

        # Count tasks for each category
        tasks_by_category = Task.objects.filter(user=user).values('category__name', 'category__color').annotate(
            count=Count('id'),
        ).order_by('category__name')

        # Count tasks where list is None
        tasks_in_backlog = Task.objects.filter(user=user, list__isnull=True).count()

        # Construct response
        return Response({
            'tasks_in_lists': list(tasks_in_lists),  # Convert to list for JSON serialization
            'tasks_by_priority': list(tasks_by_priority),  # Convert to list
            'tasks_in_backlog': tasks_in_backlog,
            'tasks_by_category': list(tasks_by_category)
        })

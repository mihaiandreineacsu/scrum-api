"""
Views for the list APIs.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Max, Prefetch

from core.models import List, Task
from list import serializers


class ListViewSet(viewsets.ModelViewSet):
    """View for manage list APIs."""

    serializer_class = serializers.ListSerializer
    queryset = List.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve list for authenticated user."""
        # Prefetch related tasks to optimize query performance
        return self.queryset.filter(user=self.request.user).prefetch_related(
            Prefetch('tasks', queryset=Task.objects.order_by('-position'))
        ).order_by('-id')

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
        list_instance = self.get_object()
        new_position = request.data.get("position")

        if new_position is not None:
            try:
                new_position = int(new_position)  # Ensure it's an integer
                if list_instance.position != new_position:
                    # Check if a list exists at the new position within the same board
                    target_list = List.objects.get(
                        board=list_instance.board, position=new_position
                    )
                    # Swap positions
                    List.swap_positions(list_instance, target_list)
            except (ValueError, List.DoesNotExist):
                # Handle invalid input or the case where no list exists with the new position
                # You can return an appropriate response here if needed
                return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Create a new list."""
        serializer.save(user=self.request.user)

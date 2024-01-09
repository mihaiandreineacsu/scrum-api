"""
Views for the list APIs.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Max, Prefetch
from django.db import IntegrityError

from core.models import List, Task, Board
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
        new_board = request.data.pop("board", list_instance.board)
        new_position = request.data.pop("position")

        change_board = new_board != list_instance.board
        change_position = new_position is not None and new_position != list_instance.position

        if change_board:
            try:
                max_position = List.objects.filter(board=new_board).aggregate(Max("position"))["position__max"]
                max_position = (max_position or 0) + 1
                new_board_instance = Board.objects.get(id=new_board)
                List.swap_parent(list_instance, new_board_instance, max_position)
            except ValueError:
                return Response("Invalid value type", status=status.HTTP_400_BAD_REQUEST)
            except IntegrityError:
                return Response("Request did not end successfully", status=status.HTTP_409_CONFLICT)
            except Board.DoesNotExist:
                List.swap_parent(list_instance, new_parent=None, new_position=max_position)

        if change_position:
            try:
                new_position = int(new_position)
                target_list = List.objects.get(board=new_board, position=new_position)
                List.swap_positions(list_instance, target_list)
            except ValueError as e:
                return Response(f"Invalid value type: {e}", status=status.HTTP_400_BAD_REQUEST)
            except IntegrityError as e:
                return Response(f"Request did not end successfully: {e}", status=status.HTTP_409_CONFLICT)
            except Task.DoesNotExist as e:
                return Response(f"Bad Request: {e}", status=status.HTTP_404_NOT_FOUND)

        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Create a new list."""
        serializer.save(user=self.request.user)

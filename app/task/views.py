"""
Views for the task APIs.
"""
import json
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Task, List
from task import serializers
from django.db.models import Max, Min
from django.db import IntegrityError


class TaskViewSet(viewsets.ModelViewSet):
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
        task_instance = self.get_object()
        new_position = request.data.pop("position", None)
        new_list = request.data.pop("list", task_instance.list)

        change_list = new_list != task_instance.list
        change_position = new_position is not None and new_position != task_instance.position

        if change_list:
            try:
                max_position = Task.objects.filter(list=new_list).aggregate(Max("position"))["position__max"]
                max_position = (max_position or 0) + 1
                new_list_instance = List.objects.get(id=new_list)
                Task.swap_parent(task_instance, new_list_instance, max_position)
            except ValueError:
                return Response("Invalid value type", status=status.HTTP_400_BAD_REQUEST)
            except IntegrityError:
                return Response("Request did not end successfully", status=status.HTTP_409_CONFLICT)
            except List.DoesNotExist:
                Task.swap_parent(task_instance, new_parent=None, new_position=max_position)

        if change_position:
            try:
                new_position = int(new_position)
                target_task = Task.objects.get(list=new_list, position=new_position)
                Task.swap_positions(task_instance, target_task)
            except ValueError as e:
                return Response(f"Invalid value type: {e}", status=status.HTTP_400_BAD_REQUEST)
            except IntegrityError as e:
                return Response(f"Request did not end successfully: {e}", status=status.HTTP_409_CONFLICT)
            except Task.DoesNotExist as e:
                return Response(f"Bad Request: {e}", status=status.HTTP_404_NOT_FOUND)

        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Create a new task."""
        task = serializer.save(user=self.request.user)
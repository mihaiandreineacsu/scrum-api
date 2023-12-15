"""
Views for the task APIs.
"""
import json
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Task
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
        queryset = self.queryset.filter(user=self.request.user)
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
        list = request.data.get("list")
        max_position = Task.objects.filter(list=list).aggregate(Max("position"))[
            "position__max"
        ]
        request.data.update({"position": (max_position or 0) + 1})
        return super().create(request, *args)

    def update(self, request, *args, **kwargs):
        # major difference, when we also wanna change the list
        # we wanna update when different position as the instance has been posted
        task_instance = self.get_object()
        new_position = request.data.get("position")
        list = request.data.get("list", task_instance.list)

        print(
            "Update Task {} at position {}, to position {} in list {}".format(
                task_instance, task_instance.position, new_position, list
            )
        )

        # if list != task_instance.list:
        #     self.swap_list(list, new_position, task_instance)
        # elif new_position is not None:
        #     self.swap_position(new_position, task_instance)

        if new_position is not None or list != task_instance.list:
            try:
                new_position = int(new_position)  # Ensure it's an integer
                if task_instance.position != new_position:
                    # Check if a task exists at the new position within the same list
                    target_task = Task.objects.get(list=list, position=new_position)
                    print(
                        "Target task {} at position {} in list {}".format(
                            target_task, target_task.position, target_task.list
                        )
                    )
                    # Swap positions
                    Task.swap_positions(task_instance, target_task)
            except (ValueError, Task.DoesNotExist, IntegrityError):
                # Handle invalid input or the case where no list exists with the new position
                # You can return an appropriate response here if needed
                return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)

            # if False and not list == task_instance.list:
            #     target_task = Task.objects.get(list=list, position=task_instance.position)
            #     print(
            #         "Target task {} at position {} in list {}".format(
            #             target_task, target_task.position, target_task.list
            #         )
            #     )

            # try:
            #     return super().update(request, *args, **kwargs)
            # except IntegrityError:
            #     min_position = Task.objects.filter(list=list).aggregate(Min("position"))[
            #         "position__min"
            #     ]
            #     return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Create a new task."""
        task = serializer.save(user=self.request.user)

    def swap_position(self, new_position, task_instance):
        pass

    def swap_list(self, new_list, new_position, task_instance):
        pass
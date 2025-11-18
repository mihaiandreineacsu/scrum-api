# src/common/serializers_base.py
from typing import TYPE_CHECKING
from rest_framework.viewsets import ModelViewSet


if TYPE_CHECKING:
    from core.models import Board, Category, Contact, ListOfTasks, Subtask, Task, User

    BoardModelViewSet = ModelViewSet[Board]
    CategoryModelViewSet = ModelViewSet[Category]
    ContactModelViewSet = ModelViewSet[Contact]
    ListOfTasksModelViewSet = ModelViewSet[ListOfTasks]
    SubtaskModelViewSet = ModelViewSet[Subtask]
    TaskModelViewSet = ModelViewSet[Task]
    UserModelViewSet = ModelViewSet[User]
else:
    BoardModelViewSet = ModelViewSet
    CategoryModelViewSet = ModelViewSet
    ContactModelViewSet = ModelViewSet
    ListOfTasksModelViewSet = ModelViewSet
    SubtaskModelViewSet = ModelViewSet
    TaskModelViewSet = ModelViewSet
    UserModelViewSet = ModelViewSet

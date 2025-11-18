# src/common/serializers_base.py
from typing import TYPE_CHECKING
from rest_framework.serializers import BaseSerializer, ModelSerializer


if TYPE_CHECKING:
    from core.models import Board, Category, Contact, ListOfTasks, Subtask, Task, User

    ModelSerializerMetaBase = ModelSerializer.Meta

    BoardModelSerializer = ModelSerializer[Board]
    BoardBasedSerializer = BaseSerializer[Board]

    CategoryModelSerializer = ModelSerializer[Category]
    CategoryBasedSerializer = BaseSerializer[Category]

    ContactModelSerializer = ModelSerializer[Contact]
    ContactBasedSerializer = BaseSerializer[Contact]

    ListOfTasksModelSerializer = ModelSerializer[ListOfTasks]
    ListOfTasksBasedSerializer = BaseSerializer[ListOfTasks]

    SubtaskModelSerializer = ModelSerializer[Subtask]
    SubtaskBasedSerializer = BaseSerializer[Subtask]

    TaskModelSerializer = ModelSerializer[Task]
    TaskBasedSerializer = BaseSerializer[Task]

    UserModelSerializer = ModelSerializer[User]
    UserBasedSerializer = BaseSerializer[User]
else:

    class ModelSerializerMetaBase:
        """Dummy base class for Django runtime."""

        pass

    BoardModelSerializer = ModelSerializer
    BoardBasedSerializer = BaseSerializer

    CategoryModelSerializer = ModelSerializer
    CategoryBasedSerializer = BaseSerializer

    ContactModelSerializer = ModelSerializer
    ContactBasedSerializer = BaseSerializer

    ListOfTasksModelSerializer = ModelSerializer
    ListOfTasksBasedSerializer = BaseSerializer

    SubtaskModelSerializer = ModelSerializer
    SubtaskBasedSerializer = BaseSerializer

    TaskModelSerializer = ModelSerializer
    TaskBasedSerializer = BaseSerializer

    UserModelSerializer = ModelSerializer
    UserBasedSerializer = BaseSerializer

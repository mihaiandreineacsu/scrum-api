from typing import TYPE_CHECKING, Any, TypeVar, override

from django.db import models
from rest_framework.authtoken.models import Token
from rest_framework.serializers import BaseSerializer, ModelSerializer, Serializer
from rest_framework.utils.serializer_helpers import ReturnDict

_MT = TypeVar("_MT", bound=models.Model)


class AppModelSerializer(ModelSerializer[_MT]):
    if TYPE_CHECKING:

        @property
        @override
        def data(self) -> ReturnDict[str, Any]:  # or Mapping[str, Any]
            ...


if TYPE_CHECKING:
    from core.models import Board, Category, Contact, ListOfTasks, Subtask, Task, User

    BoardModelSerializer = AppModelSerializer[Board]
    BoardBasedSerializer = BaseSerializer[Board]

    CategoryModelSerializer = AppModelSerializer[Category]
    CategoryBasedSerializer = BaseSerializer[Category]

    ContactModelSerializer = AppModelSerializer[Contact]
    ContactBasedSerializer = BaseSerializer[Contact]

    ListOfTasksModelSerializer = AppModelSerializer[ListOfTasks]
    ListOfTasksBasedSerializer = BaseSerializer[ListOfTasks]

    SubtaskModelSerializer = AppModelSerializer[Subtask]
    SubtaskBasedSerializer = BaseSerializer[Subtask]

    TaskModelSerializer = AppModelSerializer[Task]
    TaskBasedSerializer = BaseSerializer[Task]

    UserModelSerializer = AppModelSerializer[User]
    UserBasedSerializer = BaseSerializer[User]

    TokenAuthSerializer = Serializer[Token]
else:

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

    TokenAuthSerializer = Serializer[Token]

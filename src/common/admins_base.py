from typing import TYPE_CHECKING

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import AbstractUser

if TYPE_CHECKING:
    from core.models import Board, Category, Contact, ListOfTasks, Subtask, Task

    SubtaskModelAdmin = admin.ModelAdmin[Subtask]
    TaskModelAdmin = admin.ModelAdmin[Task]
    ContactModelAdmin = admin.ModelAdmin[Contact]
    CategoryModelAdmin = admin.ModelAdmin[Category]
    ListOfTasksModelAdmin = admin.ModelAdmin[ListOfTasks]
    BoardModelAdmin = admin.ModelAdmin[Board]
    UserModelAdmin = UserAdmin[AbstractUser]
else:
    SubtaskModelAdmin = admin.ModelAdmin
    TaskModelAdmin = admin.ModelAdmin
    ContactModelAdmin = admin.ModelAdmin
    CategoryModelAdmin = admin.ModelAdmin
    ListOfTasksModelAdmin = admin.ModelAdmin
    BoardModelAdmin = admin.ModelAdmin
    UserModelAdmin = UserAdmin

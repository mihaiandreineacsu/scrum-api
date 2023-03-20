"""
URL mappings for the task app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from subtask import views

router = DefaultRouter()
router.register('subtasks', views.SubtaskViewSet)

app_name = 'subtask'

urlpatterns = [
    path('', include(router.urls)),
]

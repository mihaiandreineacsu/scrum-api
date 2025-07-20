"""
URL mappings for the board app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from board import views

router = DefaultRouter()
router.register('boards', views.BoardViewSet)

app_name = 'board'

urlpatterns = [
    path('', include(router.urls)),
]

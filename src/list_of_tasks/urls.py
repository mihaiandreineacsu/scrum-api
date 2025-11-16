"""
URL mappings for the list app.
"""

from django.urls import (
    include,
    path,
)
from rest_framework.routers import DefaultRouter

from list_of_tasks import views

router = DefaultRouter()
router.register("lists", views.ListViewSet, basename="list")

app_name = "list"

urlpatterns = [
    path("", include(router.urls)),
]

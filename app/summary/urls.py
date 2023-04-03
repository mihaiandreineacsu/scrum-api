"""
URL mappings for the summary app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from summary import views

router = DefaultRouter()
router.register('summary', views.SummaryViewSet)

app_name = 'summary'

urlpatterns = [
    path('', include(router.urls)),
]

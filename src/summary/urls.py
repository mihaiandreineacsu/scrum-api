"""
URL mappings for the summary app.
"""
from django.urls import (  # include,
    path,
)

from summary import views

# from rest_framework.routers import DefaultRouter


# router = DefaultRouter()
# router.register('summary', views.SummaryView)

app_name = 'summary'

urlpatterns = [
    path('', views.SummaryView.as_view(), name='summary'),
]

"""
URL mappings for contact API.
"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from contact import views

router = DefaultRouter()
router.register('contacts', views.ContactViewSet)

app_name = 'contact'

urlpatterns = [
    path('', include(router.urls)),
]

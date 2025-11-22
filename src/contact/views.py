"""
Views for the contact APIs.
"""

from typing import override

from django.db.models.functions import Lower
from django.db.models.query import QuerySet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from common.serializers_base import ContactBasedSerializer
from common.views_base import ContactModelViewSet
from contact.serializers import ContactSerializer
from core.models import Contact


class ContactViewSet(ContactModelViewSet):
    """View for manage contact APIs."""

    serializer_class = ContactSerializer
    queryset = Contact.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @override
    def get_queryset(self) -> QuerySet[Contact]:
        """Retrieve contacts for authenticated user."""
        assert self.queryset is not None
        return self.queryset.filter(user=self.request.user).order_by(Lower("name"))

    @override
    def perform_create(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, serializer: ContactBasedSerializer
    ):
        """Create a new contact."""
        _ = serializer.save(user=self.request.user)

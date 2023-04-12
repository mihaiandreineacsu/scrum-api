"""
Views for the contact APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Contact
from contact import serializers


class ContactViewSet(viewsets.ModelViewSet):
    """View for manage contact APIs."""
    serializer_class = serializers.ContactSerializer
    queryset = Contact.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve contacts for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.ContactSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new contact."""
        serializer.save(user=self.request.user)

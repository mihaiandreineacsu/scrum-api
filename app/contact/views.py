"""
Views for the contact APIs.
"""
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Contact
from contact import serializers

from django.db.models.functions import Lower


class ContactViewSet(viewsets.ModelViewSet):
    """View for manage contact APIs."""
    serializer_class = serializers.ContactSerializer
    queryset = Contact.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve contacts for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by(Lower('name'))

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.ContactSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new contact."""
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Create a new contact with unique email for the user."""
        user = self.request.user
        email = request.data.get('email')
        if Contact.objects.filter(user=user, email=email).exists():
            return Response(
                {'detail': 'A contact with this email already exists for this user.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)

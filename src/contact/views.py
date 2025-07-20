"""
Views for the contact APIs.
"""

from django.db.models.functions import Lower
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from contact import serializers
from core.models import Contact


class ContactViewSet(viewsets.ModelViewSet):
    """View for manage contact APIs."""

    serializer_class = serializers.ContactSerializer
    queryset = Contact.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve contacts for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by(Lower("name"))

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == "list":
            return serializers.ContactSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new contact."""
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Create a new contact with unique email/phone_number for the user."""
        user = self.request.user
        email = request.data.get("email")
        name = request.data.get("name")
        phone_number = request.data.get("phone_number")

        if not any([email, name, phone_number]):
            return Response(
                {
                    "detail": "At least one of email, name, or phone number must be provided."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if email and Contact.objects.filter(user=user, email=email).exists():
            return Response(
                {"detail": "A contact with this email already exists for this user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (
            phone_number
            and Contact.objects.filter(user=user, phone_number=phone_number).exists()
        ):
            return Response(
                {
                    "detail": "A contact with this phone number already exists for this user."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Update a new contact with unique email/phone_number for the user."""
        user = self.request.user
        email = request.data.get("email")
        name = request.data.get("name")
        phone_number = request.data.get("phone_number")

        if not any([email, name, phone_number]):
            return Response(
                {
                    "detail": "At least one of email, name, or phone number must be provided."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if email and Contact.objects.filter(user=user, email=email).exists():
            return Response(
                {"detail": "A contact with this email already exists for this user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (
            phone_number
            and Contact.objects.filter(user=user, phone_number=phone_number).exists()
        ):
            return Response(
                {
                    "detail": "A contact with this phone number already exists for this user."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().update(request, *args, **kwargs)

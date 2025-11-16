"""
Views for the contact APIs.
"""

from typing import Any, override

from django.db.models.functions import Lower
from django.db.models.query import QuerySet
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from contact.serializers import ContactSerializer
from core.models import Contact, User


class ContactViewSet(ModelViewSet[Contact]):
    """View for manage contact APIs."""

    serializer_class: type[ContactSerializer] = ContactSerializer
    queryset: QuerySet[Contact, Contact] = Contact.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @override
    def get_queryset(self) -> QuerySet[Contact, Contact]:
        """Retrieve contacts for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by(Lower("name"))

    @override
    def get_serializer_class(self) -> type[ContactSerializer]:
        """Return the serializer class for request."""
        if self.action == "list":
            return ContactSerializer

        return self.serializer_class

    @override
    def perform_create(self, serializer: ContactSerializer):
        """Create a new contact."""
        _ = serializer.save(user=self.request.user)

    @override
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Create a new contact with unique email/phone_number for the user."""
        validation_response = self._validate_unique_contact(request)
        if validation_response:
            return validation_response
        return super().create(request, *args, **kwargs)

    @override
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Update a new contact with unique email/phone_number for the user."""
        validation_response = self._validate_unique_contact(request)
        if validation_response:
            return validation_response
        return super().update(request, *args, **kwargs)

    def _validate_unique_contact(self, request: Request) -> Response | None:
        """Validate that the contact's email and phone number are unique for the user."""
        user: User = self.request.user
        email: str = request.data.get("email", "")
        name: str = request.data.get("name", "")
        phone_number: str = request.data.get("phone_number", "")

        validation_error = ""

        if not any([email, phone_number, name]):
            validation_error = (
                "At least one of email, name, or phone number must be provided."
            )

        if email and Contact.objects.filter(user=user, email=email).exists():
            validation_error = "A contact with this email already exists for this user."

        if (
            phone_number
            and Contact.objects.filter(user=user, phone_number=phone_number).exists()
        ):
            validation_error = (
                "A contact with this phone number already exists for this user."
            )

        if validation_error:
            return Response({"detail": validation_error}, status=HTTP_400_BAD_REQUEST)

        return None

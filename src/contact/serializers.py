"""
Serializers for Contact APIs
"""

from typing import Any
from rest_framework.serializers import ModelSerializer
from rest_framework.utils.serializer_helpers import ReturnDict

from core.models import Contact


class ContactSerializer(ModelSerializer[Contact]):
    """Serializer for contacts."""

    data: ReturnDict[str, Any]

    class Meta:
        model = Contact
        fields = ["id", "email", "name", "phone_number", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

"""
Serializers for Contact APIs
"""

from typing import TYPE_CHECKING

from rest_framework.serializers import ModelSerializer

from common.serializers_base import ContactModelSerializer
from core.models import Contact


class ContactSerializer(ContactModelSerializer):
    """Serializer for contacts."""

    class Meta:
        model = Contact
        fields = ["id", "email", "name", "phone_number", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    if TYPE_CHECKING:
        Meta: type[ModelSerializer.Meta]

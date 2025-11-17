"""
Serializers for Contact APIs
"""

from rest_framework.serializers import ModelSerializer

from core.models import Contact


class ContactSerializer(ModelSerializer):
    """Serializer for contacts."""

    class Meta:
        model = Contact
        fields = ["id", "email", "name", "phone_number", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

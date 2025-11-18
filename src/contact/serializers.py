"""
Serializers for Contact APIs
"""

from common.serializers_base import ContactModelSerializer, ModelSerializerMetaBase
from core.models import Contact


class ContactSerializer(ContactModelSerializer):
    """Serializer for contacts."""

    class Meta(ModelSerializerMetaBase):
        model = Contact
        fields = ["id", "email", "name", "phone_number", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

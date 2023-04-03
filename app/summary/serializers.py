"""
Serializers for Summary APIs
"""
from rest_framework import serializers

from core.models import Summary


class SummarySerializer(serializers.ModelSerializer):
    """Serializer for summary."""

    class Meta:
        model = Summary
        fields = ['id',]
        read_only_fields = ['id']

"""
Serializers for the user API View.
"""

from typing import Any, override

from django.contrib.auth import authenticate
from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "name",
            "image",
            "id",
            "created_at",
            "updated_at",
            "is_guest",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "is_guest"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    @override
    def create(self, validated_data: Any) -> User:
        """Create and return a user with encrypted password."""
        return User.objects.create_user(**validated_data)

    @override
    def update(self, instance: User, validated_data: Any) -> User:
        """Update and return user."""
        password = validated_data.pop("password", None)
        user: User = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    @override
    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """Validate and authenticate the user."""
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )
        if not user:
            raise serializers.ValidationError(
                {"detail": ["Unable to authenticate with provided credentials."]},
                code="authorization",
            )
        attrs["user"] = user
        return attrs


class UserImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to users."""

    class Meta:
        model = User
        fields = ["id", "image"]
        read_only_fields = ["id"]
        extra_kwargs = {"image": {"required": "True"}}

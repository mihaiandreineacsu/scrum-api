"""
Views for the user API.
"""

from typing import Any, TypeAlias, override

from django.contrib.auth.models import AnonymousUser
from rest_framework import (
    authentication,
    permissions,
    status,
)
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from common.views_base import (
    UserCreateAPIView,
    UserModelViewSet,
    UserRetrieveUpdateDestroyAPIView,
)
from core.models import User
from user.permissions import IsNotGuestUser
from user.serializers import AuthTokenSerializer, UserImageSerializer, UserSerializer


class CreateUserView(UserCreateAPIView):
    """Create a new user in the system."""

    serializer_class = UserSerializer


class CreateGuestUserView(APIView):
    """Create a new guest user in the system."""

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        user = User.objects.create_guest_user()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_201_CREATED)


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(UserRetrieveUpdateDestroyAPIView):
    """Manage the authenticated user."""

    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsNotGuestUser]

    @override
    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user

    @override
    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Handle user deletion."""
        user = self.get_object()
        _ = user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserUploadImageView(UserModelViewSet):
    serializer_class = UserImageSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsNotGuestUser]

    @override
    def get_object(self):
        """Retrieve and return the authenticated user."""
        if isinstance(self.request.user, AnonymousUser):
            raise ValueError("Should not happen")
        return self.request.user

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request: Request):
        """Upload an image to user."""
        # print("Absolute URI: %s", request.build_absolute_uri())
        # print("Host: %s", request.get_host())
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)

        if serializer.is_valid():
            _ = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

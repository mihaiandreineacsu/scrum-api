"""
Views for the user API.
"""
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import (
    generics,
    authentication,
    permissions,
    viewsets,
    status,
)
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.settings import api_settings
from rest_framework.authtoken.models import Token

from user.serializers import UserSerializer, AuthTokenSerializer, UserImageSerializer
from django.contrib.auth import get_user_model
from user.permissions import IsNotGuestUser



class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    serializer_class = UserSerializer


class CreateGuestUserView(APIView):
    def post(self, request, *args, **kwargs):
        user = get_user_model().objects.create_guest_user()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""

    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsNotGuestUser]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user

    def get_serializer_class(self):
        """Return the serializer class for request."""
        return self.serializer_class

    def delete(self, request, *args, **kwargs):
        """Handle user deletion."""
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserUploadImageView(viewsets.ModelViewSet):
    serializer_class = UserImageSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsNotGuestUser]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user

    def get_serializer_class(self):
        """Return the serializer class for request."""
        return self.serializer_class

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        """Upload an image to user."""
        print("Absolute URI: %s", request.build_absolute_uri())
        print("Host: %s", request.get_host())
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

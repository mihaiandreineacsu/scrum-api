from typing import cast, override

from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from core.models import User


class IsNotGuestUser(permissions.BasePermission):
    """
    Custom permission to only allow non-guest users to update their information.
    """

    @override
    def has_permission(self, request: Request, view: APIView):
        is_guest = (
            not isinstance(request.user, AnonymousUser)
            and cast(User, request.user).is_guest
        )
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == "DELETE" and is_guest:
            return True

        return not is_guest

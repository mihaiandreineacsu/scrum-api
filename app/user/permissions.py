from rest_framework import permissions


class IsNotGuestUser(permissions.BasePermission):
    """
    Custom permission to only allow non-guest users to update their information.
    """

    def has_permission(self, request, view):
        # Check if the request is a safe method (GET, HEAD, OPTIONS)
        # which is allowed for guest users as well.
        if request.method in permissions.SAFE_METHODS or request.method == 'DELETE':
            return True

        # Allow DELETE method only if the user is not a guest
        if request.method == 'DELETE':
            return not request.user.is_guest

        # For methods other than safe methods, check if the user is not a guest
        return not request.user.is_guest

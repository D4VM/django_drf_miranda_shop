from rest_framework import permissions

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")
AUTHENTICATED_METHODS = ("POST",)


class OrderPermissions(permissions.BasePermission):
    """
    Custom permission to only allow authenticated users to view and post orders
    Admin users have full access.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if (
                request.method in SAFE_METHODS
                or request.method in AUTHENTICATED_METHODS
            ):
                return True
            elif request.user.is_staff:
                return True
        return False

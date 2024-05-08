from rest_framework import permissions

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")
AUTHENTICATED_METHODS = ("POST",)


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to edit objects.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        if request.method in AUTHENTICATED_METHODS:
            return request.user.is_authenticated

        return request.user.is_authenticated and request.user.is_staff

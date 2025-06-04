from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to admin (is_staff=True) users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_staff

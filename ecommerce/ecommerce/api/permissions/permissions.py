from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to allow only admin users to create a user.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated and has the admin role
        return request.user.is_authenticated and request.user.user_type == "ADMIN"

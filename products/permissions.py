from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, BasePermission


class IsProductVendor(IsAuthenticated):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.user_type == 'CUSTOMER'
        )
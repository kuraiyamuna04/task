from rest_framework.permissions import BasePermission

from app.models import CustomUser


class RequiredAdmin(BasePermission):
    def has_permission(self, request, view):
        try:
            user = request.user.role
            if user == CustomUser.Admin:
                return True
        except ValueError:
            raise ValueError("No data found")


class RequiredManager(BasePermission):
    def has_permission(self, request, view):
        try:
            user = request.user.role
            if user == CustomUser.Manager:
                return True
        except ValueError:
            raise ValueError("No data found")

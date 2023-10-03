from rest_framework.permissions import BasePermission


class RequiredAdmin(BasePermission):
    def has_permission(self, request, view):
        try:
            user = request.user.role
            if str(user) == 'A':
                return True
        except Exception as e:
            print(e)


class RequiredManager(BasePermission):
    def has_permission(self, request, view):
        try:
            user = request.user.role
            if str(user) == 'M':
                return True
        except Exception as e:
            print(e)

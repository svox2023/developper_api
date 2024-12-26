from rest_framework.permissions import BasePermission

class IsMechanic(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'mecanicien')

class IsClient(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'client')

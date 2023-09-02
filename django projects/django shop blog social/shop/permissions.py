from rest_framework.permissions import BasePermission

class IsStaffAccessPermissions(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_staff)
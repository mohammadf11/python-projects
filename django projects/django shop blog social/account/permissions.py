from rest_framework.permissions import BasePermission

class IsStaffAccessPermissions(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_staff)


class IsStaffOrOwnerAccessPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_staff or obj.user == request.user)

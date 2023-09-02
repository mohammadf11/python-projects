from rest_framework.permissions import BasePermission

class IsStaffAccessPermissions(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_staff)

class IsSuperuserOrOwnerAccessMixins(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_staff)
    
    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_superuser or obj.author == request.user)
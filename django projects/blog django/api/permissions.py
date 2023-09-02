from rest_framework.permissions import BasePermission

class IsSuperuserAuthorAccessPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_superuser or request.user.is_author)

class IsSuperuserAuthorAccessModifyPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_superuser or request.user.is_author)

    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_superuser or request.user.is_author and obj.author == request.user)

class IsStaffAccessPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_staff )
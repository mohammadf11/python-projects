from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model

User = get_user_model()

class LogoutPermisson(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or not request.user.is_authenticated

class IsStaffOrOwnerAccessPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_staff or obj.user == request.user)

from rest_framework.permissions import BasePermission
from . serializers import FollowSerializers , LikeSerializers


class IsStaffAccessPermissions(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_staff)

class IsStaffOrOwnerAccessPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_staff or obj.user == request.user)

class IsStaffOrFollowerPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE' and not request.user.is_staff:
            return bool(obj.follower == request.user)
        return True
                    

class IsStaffOrOwnerLikePermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE' and not request.user.is_staff:
            return bool(obj.user == request.user)
        return True

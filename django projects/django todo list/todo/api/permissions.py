from rest_framework.permissions import BasePermission
class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return  request.user == obj.user or request.user.is_staff
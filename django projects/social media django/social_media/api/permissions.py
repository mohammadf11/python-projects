from rest_framework.permissions import BasePermission
from ..models import Like , Post , Follow
from rest_framework.response import Response
from . import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class ModifyAccessPermisson(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_staff or request.user == obj.user)

class ModifyAccessLikePermisson(ModifyAccessPermisson):
    pass



class OneLikePermissions(BasePermission):
    def has_permission(self, request, view):
        user = request.data.get('user')
        if  not request.user.is_staff:
            user = request.user.id
        post = request.data.get('post')
        if post and user:
            is_like = Like.objects.filter(user__id = int(user), post__id = int(post)).exists()
            if is_like and not request.user.is_staff:
                return False
        return True


class ModifyAccessFollowPermisson(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_staff or request.user == obj.follower)


class OneFollowPermissions(BasePermission):
    def has_permission(self, request, view):
        follower = request.data.get('follower')
        if  not request.user.is_staff:
            follower = request.user.id
        following = request.data.get('following')
        if follower and following:
            is_follow = Follow.objects.filter(follower__id = int(follower), following__id = int(following)).exists()
            if is_follow and not request.user.is_staff:
                return False
        return True

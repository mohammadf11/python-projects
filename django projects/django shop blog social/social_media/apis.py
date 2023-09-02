from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from . import permissions
from . import serializers
from .models import Post, Like, Follow


class PostModelViewSet(ModelViewSet):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_staff or self.request.method == 'GET':
            return serializers.StaffPostSerializers
        return serializers.PostSerializers

    def create(self, request):
        serializer = self.get_serializer_class()
        serializer_data = serializer(data=request.data)
        if serializer_data.is_valid():
            if not request.user.is_staff:
                serializer_data.save(user = request.user)
            else:  
                serializer_data.save()
            return Response(serializer_data.data, status=status.HTTP_200_OK)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated,
                                  permissions.IsStaffOrOwnerAccessPermissions]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class LikeModelViewSet(ModelViewSet):
    queryset = Like.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_staff or self.request.method == "GET":
            return serializers.StaffLikeSerializers
        return serializers.LikeSerializers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serializer_data = serializer(data=request.data)
        if serializer_data.is_valid():
            post = serializer_data.validated_data['post']
            if not request.user.is_staff:
                user = request.user
            else:
                user = serializer_data.validated_data['user']
            if not Like.objects.filter(user=user, post=post).exists():
                Like.objects.create(user=user, post=post)
            else:
                return Response({"messages": "you like this post already"})
            return Response(serializer_data.data, status=status.HTTP_200_OK)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated,
                                  permissions.IsStaffOrOwnerLikePermissions]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated,
                                  permissions.IsStaffAccessPermissions]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class FollowModelViewSet(ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = serializers.FollowSerializers

    def get_serializer_class(self):
        if self.request.user.is_staff or self.request.method == "GET":
            return serializers.StaffFollowSerializers
        return serializers.FollowSerializers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serializer_data = serializer(data=request.data)
        if serializer_data.is_valid():
            following = serializer_data.validated_data['following']
            if not request.user.is_staff:
                follower = request.user
            else:
                follower = serializer_data.validated_data['follower']

            if not Follow.objects.filter(follower=follower, following=following).exists():
                Follow.objects.create(follower=follower, following=following)
            else:
                return Response({"messages": "you follow this user already"})
            return Response(serializer_data.data, status=status.HTTP_200_OK)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated,
                                  permissions.IsStaffOrFollowerPermissions]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated,
                                  permissions.IsStaffAccessPermissions]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

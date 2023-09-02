from rest_framework.viewsets import ModelViewSet
from . import serializers
from ..models import Post , Like , Follow
from rest_framework.permissions import  AllowAny , IsAuthenticated , IsAdminUser
from . import permissions
# from rest_framework.authentication import SessionAuthentication

# class CsrfExemptSessionAuthentication(SessionAuthentication):

#     def enforce_csrf(self, request):
#         return

# class ListCreatePostApiView(generics.ListCreateAPIView):
#     queryset =  Post.objects.all()
#     serializer_class = serializers.PostSerializer

# class RetrieveUpdateDestroyPostAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset =  Post.objects.all()
#     serializer_class = serializers.PostSerializer


class PostViewSet(ModelViewSet):
    queryset =  Post.objects.all()
    serializer_class = serializers.PostSerializer


    def perform_create(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            serializer.save(user = self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_class = [AllowAny]
        elif self.action == 'create':
            permission_class = [IsAuthenticated]
        else:
            permission_class = [IsAuthenticated ,permissions.ModifyAccessPermisson ]

        return [permission() for permission in permission_class]



    

class LikeViewSet(ModelViewSet):
    queryset =  Like.objects.all()
    serializer_class = serializers.Likeserializer

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            serializer.save(user = self.request.user)

    def get_permissions(self):
        if self.action == 'create' :
            permission_class =  [IsAuthenticated , permissions.OneLikePermissions]
        elif self.action == 'destroy':
            permission_class = [IsAuthenticated , permissions.ModifyAccessLikePermisson ]
        else:
            permission_class = [IsAdminUser]

        return [permission() for permission in permission_class]




class FollowViewSet(ModelViewSet):
    queryset =  Follow.objects.all()
    serializer_class = serializers.Followserializer

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            serializer.save(follower = self.request.user)

    def get_permissions(self):
        if self.action == 'create' :
            permission_class =  [IsAuthenticated , permissions.OneFollowPermissions]
        elif self.action == 'destroy':
            permission_class = [IsAuthenticated , permissions.ModifyAccessFollowPermisson ]
        else:
            permission_class = [IsAdminUser]

        return [permission() for permission in permission_class]
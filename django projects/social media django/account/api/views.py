from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser , IsAuthenticated , AllowAny
from . import serializers
from . import permissions
from django.contrib.auth import get_user_model
from ..models import Profile

User = get_user_model()

# class UserViewSet(ModelViewSet):
#     authentication_classes = [CsrfExemptSessionAuthentication]
#     serializer_class = serializers.UserSerializer
#     queryset = User.objects.all()

#     def get_permissions(self):
#         if self.action == 'create':
#             permission_clsss = [permissions.LogoutPermisson]
#         else:
#             permission_clsss = [IsAdminUser]
        
#         return [permission() for permission in permission_clsss]

    


    # serializer_class = serializers.RegisterSerializer
    # def post(self, request):
    #     srz_data = self.serializer_class(data=request.data)
    #     if srz_data.is_valid():
    #         srz_data.save()
    #         return Response(srz_data.data, status=status.HTTP_201_CREATED)
    #     return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAuthenticated,
                                  IsAdminUser]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated,
                                  permissions.IsStaffOrOwnerAccessPermissions]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]



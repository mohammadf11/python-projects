from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.response import Response
from rest_framework import status
from . import permissions
from . import serializers
from .models import Article , ArticleCategory

class ArticleModelViewSet(ModelViewSet):
    queryset = Article.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.CreateArticleSerializers
        return serializers.ArticleSerializers

    def create(self, request):
        serializer = self.get_serializer_class()
        serializer_data = serializer(data = request.data)
        if serializer_data.is_valid():
            serializer_data.save(author = request.user)
            return Response(serializer_data.data , status=status.HTTP_201_CREATED)
        return Response(serializer_data.errors , status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated , permissions.IsStaffAccessPermissions]
        elif self.action in ['update' , 'partial_update' ,'destroy']:
            permission_classes = [IsAuthenticated , permissions.IsSuperuserOrOwnerAccessPermissions]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class ArticleCategoryModelViewSet(ModelViewSet):
    queryset = ArticleCategory.objects.all()
    serializer_class = serializers.ArticleCategorySerializers
    permission_classes = [IsAuthenticated ,permissions.IsStaffAccessPermissions]




from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import ListCreateAPIView , RetrieveUpdateDestroyAPIView


from . import permissions
from . import serializers
from blog.models import Article , Category

# Create your views here.


class UserProfileApiView(ListAPIView):
    serializer_class = serializers.ArticleSerializer
    permission_classes = (
        IsAuthenticated, permissions.IsSuperuserAuthorAccessPermission)

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)


class ArticleModelViewSet(ModelViewSet):
    serializer_class = serializers.ArticleSerializer
    queryset = Article.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category',]

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated ,permissions.IsSuperuserAuthorAccessPermission]
        elif self.action in ['update', 'destroy' , 'partial_update'] :
            permission_classes = [IsAuthenticated ,permissions.IsSuperuserAuthorAccessModifyPermission]
        else:
            permission_classes = [AllowAny]

        return [ permission() for permission in permission_classes ]

# class ArticleViewSet(ViewSet):
#     serializer_class = serializers.ArticleSerializer
#     queryset = Article.objects.all()

#     def get_permissions(self):
#         if self.action in ['create', 'update', 'delete', 'partial_update']:
#             self.permission_classes = [
#                 IsAuthenticated, permissions.IsSuperuserAuthorAccessPermission]
#         return super().get_permissions()

#     def list(self, request):
#         srz_data = self.serializer_class(instance=self.queryset, many=True)
#         return Response(srz_data.data, status=status.HTTP_200_OK)

#     def retrieve(self, request, pk):
#         srz_data = self.serializer_class(
#             instance=get_object_or_404(self.queryset, pk=pk))
#         return Response(srz_data.data, status=status.HTTP_200_OK)

#     def create(self, request):
#         srz_data = self.serializer_class(
#             data=self.request.POST)  # self.request.data
#         if srz_data.is_valid():
#             srz_data.save()
#             return Response(srz_data.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

#     def update(self, request, pk):

#         srz_data = self.serializer_class(
#             instance=get_object_or_404( self.queryset, pk=pk), 
#             data=self.request.POST, partial=True)

#         if srz_data.is_valid():
#             srz_data.save()
#             return Response(srz_data.data, status=status.HTTP_200_OK)
#         else:
#             return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

#     def partial_update(self, request, pk):
#         Response = self.update(request, pk)
#         return Response

#     def delete(self, request, pk):
#         get_object_or_404(self.queryset ,pk=pk).delete()
#         return Response({"message": "article deleted"}, status=status.HTTP_204_NO_CONTENT)

class CategoryListCreateAPIView(ListCreateAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [permissions.IsStaffAccessPermission]
        return super().get_permissions()


class CategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()
    def get_permissions(self):
        if self.request.method in ['PUT' , 'DELETE']:
            self.permission_classes = [permissions.IsStaffAccessPermission]
        return super().get_permissions()

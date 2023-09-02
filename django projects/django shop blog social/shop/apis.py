from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated , AllowAny
from . import permissions
from . import serializers
from .models import ShopCategory , Product

class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializers

    def get_permissions(self):
        if self.action in ['create' , 'update' , 'partial_update' ,'destroy']:
            permission_classes = [IsAuthenticated , permissions.IsStaffAccessPermissions]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]


class ShopCategoryModelViewSet(ModelViewSet):
    queryset = ShopCategory.objects.all()
    serializer_class = serializers.ShopCategorySerializers
    permission_classes = [IsAuthenticated , permissions.IsStaffAccessPermissions]




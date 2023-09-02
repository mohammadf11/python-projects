from rest_framework import serializers
from .models import Product , ShopCategory

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ShopCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = ShopCategory
        fields = '__all__'
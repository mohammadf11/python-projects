from django.contrib import admin
from .models import ShopCategory, Product
# Register your models here.


@admin.register(ShopCategory)
class ShopCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_editable = ['is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available']
    list_editable = ['price', 'is_available']
    list_filter = ['is_available']
    raw_id_fields = ['category']
    search_fields = ['name', 'is_available']
    prepopulated_fields = {'slug': ('name',)}

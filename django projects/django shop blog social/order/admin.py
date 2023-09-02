from django.contrib import admin
from .models import *
# Register your models here.

class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)
    can_delete = True

# Define a new User admin
@admin.register(Order)
class UserAdmin(admin.ModelAdmin):
    list_display = ['user' , 'is_paid' , 'get_total_price' ]
    inlines = (OrderItemAdmin,)
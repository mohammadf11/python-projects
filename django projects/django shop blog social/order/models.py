import imp
from pyexpat import model
from webbrowser import get
from django.db import models
from django.contrib.auth import get_user_model
from shop.models import Product
# Create your models here.
User = get_user_model()

class Order(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='orders' )
    is_paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['is_paid']

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order  , on_delete=models.CASCADE , related_name='items')
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def get_cost(self):
        return self.price * self.quantity
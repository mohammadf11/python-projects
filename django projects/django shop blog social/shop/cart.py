from django.shortcuts import get_object_or_404
from .models import Product
SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(SESSION_ID)
        if not cart:
            cart = self.session[SESSION_ID] = {}
        self.cart = cart
    
    def __len__(self):
        return len(self.cart)
    
    def __iter__(self ):
        for key in self.cart.keys():
            product = get_object_or_404(Product , id = key)
            cart = {}
            cart['product'] = product
            cart['quantity'] = self.cart[key]['quantity']
            cart['price'] = self.cart[key]['price']
            cart['total_price'] = cart['quantity'] * product.price
            yield cart

    def add_cart(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart.keys():
            self.cart[product_id] = {'quantity': 0, 'price': product.price}
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove_cart(self , product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        return sum(item['price'] * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[SESSION_ID]
        
    def save(self):
        self.session.modified = True



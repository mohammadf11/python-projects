from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models import Product
from .cart import Cart
from .forms import QuantityForm
from . import mixins
# Create your views here.


class ProductLsitView(ListView):
    template_name = 'shop/product_list.html'
    context_object_name = 'products'  # object_list
    paginate_by = 8

    def get_queryset(self):
        products =  Product.objects.availabled()
        search_input = self.request.GET.get('search_area')
        if search_input:
            products = products.filter(
                Q(name__contains=search_input) | Q(description__contains=search_input)
            )
        return products 


class ProductDetailView(DetailView):
    queryset = Product.objects.availabled()
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['quantity_form'] = QuantityForm()
        return context


class ProductCreateView(LoginRequiredMixin, mixins.IsStaffAccessMixins, CreateView):
    model = Product
    fields = ('category', 'name', 'description',
              'image', 'price', 'is_available')
    template_name = 'shop/product_create.html'
    success_url = reverse_lazy('shop:manage_product')


class ProductUpdateView(LoginRequiredMixin, mixins.IsStaffAccessMixins, UpdateView):
    model = Product
    fields = ('category', 'name', 'description',
              'image', 'price', 'is_available')
    template_name = 'shop/product_update.html'
    success_url = reverse_lazy('shop:manage_product')


class ProductDeleteView(LoginRequiredMixin, mixins.IsStaffAccessMixins, DeleteView):
    model = Product
    template_name = 'shop/product_delete.html'
    success_url = reverse_lazy('shop:manage_product')


class ManageProductView(LoginRequiredMixin, mixins.IsStaffAccessMixins, ListView):
    model = Product
    template_name = 'shop/manage_product.html'
    context_object_name = 'products'


class AddProductCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        form = QuantityForm(request.POST)
        if form.is_valid():
            product = get_object_or_404(Product, id=product_id)
            cart = Cart(request)
            cart.add_cart(product, form.cleaned_data['quantity'])
        return redirect('shop:product_list')


class RemoveProductCartView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        cart = Cart(request)
        cart.remove_cart(str(product_id))
        return redirect('shop:cart')


class CartView(LoginRequiredMixin, View):
    template_name = 'shop/cart.html'

    def get(self, request):
        cart = Cart(request)
        cart_count = len(request.session['cart'])
        return render(request, self.template_name, {'cart_count': cart_count, 'cart': cart})


# def shop(request):
#     products = Product.objects.all()
#     context ={
#         'products' :products
#     }
#     return render(request, 'shop/shop.html' , context)

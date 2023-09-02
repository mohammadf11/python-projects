from django.urls import path , include
from rest_framework import routers
from . import apis
from . import views

app_name = 'shop'

# urlpatterns = [
#     path('' , views.shop , name = 'shop')
# ]


urlpatterns = [
    path('', views.ProductLsitView.as_view(), name='product_list'),
    path('product_detail/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product_create/', views.ProductCreateView.as_view(), name='product_create'),
    path('product_update/<int:pk>/', views.ProductUpdateView.as_view(), name='product_update'),
    path('product_delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('manage_product/', views.ManageProductView.as_view(), name='manage_product'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('add_cart/<int:product_id>/' , views.AddProductCartView.as_view() , name ='add_product_cart'),
    path('remove_produce_cart/<int:product_id>/' , views.RemoveProductCartView.as_view() , name ='remove_product_cart'),

]




# api urls
router = routers.SimpleRouter()
router.register('products', apis.ProductModelViewSet , basename='products')
router.register('shop_categories', apis.ShopCategoryModelViewSet , basename='shop_categories')
urlpatterns += [
    path('shop/api/' , include(router.urls)),
]

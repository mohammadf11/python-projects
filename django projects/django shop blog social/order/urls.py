import imp
from django.urls import path
from . import views

app_name= 'order'

urlpatterns = [
    path('' , views.OrderCheckOutView.as_view() , name = 'order_verify'),
    path('order_pay/<int:order_id>' , views.OrderPayView.as_view() , name = 'order_pay'),
    path('verify/' , views.OrderVerifyView.as_view() , name = 'verify'),
]
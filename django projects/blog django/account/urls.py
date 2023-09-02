from django.urls import path
from . import views


app_name= 'account'

urlpatterns = [
    
    path('login/' , views.UserLoginView.as_view() , name = 'login'),
    path('register/' , views.UserRegisterView.as_view() , name = 'register'),
    path('logout/' , views.UserLogoutView.as_view() , name = 'logout'),
    path('profile/' , views.UserProfileView.as_view() , name = 'profile'),
]
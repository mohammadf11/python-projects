from django.urls import path , include
from . import views
from rest_framework import routers
router = routers.SimpleRouter()
# router.register('users' , views.UserViewSet , basename='users')
router.register('profiles' , views.ProfileViewSet , basename='profiles')
urlpatterns = [
    path('' ,include(router.urls))
]
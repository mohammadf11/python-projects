from django.urls import path , include
from . import views
from rest_framework import routers
router = routers.SimpleRouter()
router.register('posts' , views.PostViewSet)
router.register('likes' , views.LikeViewSet)
router.register('follows' , views.FollowViewSet)

urlpatterns = [
    # path('posts/' , views.ListCreatePostApiView.as_view() , name = 'list_create_post_api'),
    # path('posts/<int:pk>' , views.RetrieveUpdateDestroyPostAPIView.as_view() , name = 'modify_post_api'),
    path('' , include(router.urls)),

    
]
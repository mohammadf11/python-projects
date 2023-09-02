from django.urls import path , include
from rest_framework import routers
from . import apis
from . import views

app_name = 'social_media'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/update/<int:pk>/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('like_post/<int:pk>/' , views.LikePostView.as_view() , name ='like_post'),
    path('dislike_post/<int:pk>/' , views.DisLikePostView.as_view() , name ='dislike_post'),
]


# api urls
router = routers.SimpleRouter()
router.register('posts', apis.PostModelViewSet , basename='posts')
router.register('likes', apis.LikeModelViewSet , basename='likes')
router.register('follows', apis.FollowModelViewSet , basename='follows')
urlpatterns += [
    path('api/' , include(router.urls)),
]

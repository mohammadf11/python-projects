from django.urls import path , include
from . import views

app_name = 'social_media'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('create_post/', views.CreatePost.as_view(), name='create_post'),
    path('update_post/<int:pk>', views.UpdatePost.as_view(), name='update_post'),
    path('delete_post/<int:pk>', views.DeletePost.as_view(), name='delete_post'),
    path('like_post/<int:pk>' , views.LikePost.as_view() , name ='like_post'),
    path('dislike_post/<int:pk>' , views.DisLikePost.as_view() , name ='dislike_post'),
    path('social_media/api/' , include('social_media.api.urls'))



]

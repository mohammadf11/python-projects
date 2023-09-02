from django.urls  import path , include
from rest_framework import routers
from . import views



router = routers.SimpleRouter()
router.register('article', views.ArticleModelViewSet , basename='article')

app_name = 'api'

urlpatterns = [
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('' , include(router.urls)),
    path('profile/' , views.UserProfileApiView.as_view() , name = 'profile'),
    path('category/', views.CategoryListCreateAPIView.as_view() , name ='category'),
    path('category/<int:pk>/', views.CategoryRetrieveUpdateDestroyAPIView.as_view() , name ='category'),



]
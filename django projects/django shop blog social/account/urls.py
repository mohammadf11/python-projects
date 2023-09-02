from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView ,TokenVerifyView
from django.urls import path  , include
from rest_framework import routers
from . import views
from . import apis

app_name = 'account'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('verify/code/', views.UserVerifyCodeView.as_view(), name='verify_code'),

    path('profile/<int:pk>', views.ProfileView.as_view(), name='profile'),
    path('edit/profile', views.EidtProfileView.as_view(), name='edit_profile'),

    path('follow/<int:pk>', views.FollowView.as_view(), name='follow'),
    path('unfollow/<int:pk>', views.UnFollowView.as_view(), name='unfollow'),

    path('password_reset/', views.UserPasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset_done/', views.UserPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>',
         views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', views.UserPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]


#api urls
router = routers.SimpleRouter()
router.register('profiles', apis.ProfileInformationsModelViewSet)
router.register('users', apis.UserInformationsModelViewset)

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),


    path('api/register/' , apis.UserRegisterApiView.as_view() , name = 'register_api'),
    path('api/verify_code/' , apis.UserVerifyCodeApiView.as_view() , name = 'verify_code_api'),

    path('api/user/' , apis.UserInformationsApiView.as_view() , name = 'user_api'),
    path('api/', include(router.urls))
    # path('api/follow/' , apis.FollowApiView.as_view() , name = 'follow_api'),
    # path('api/unfollow/' , apis.UnFollowApiView.as_view() , name = 'unfollow_api'),

]

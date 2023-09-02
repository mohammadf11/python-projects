from django.urls import path , include
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.UserLoginView.as_view() , name = 'login'),
    path('logout/', views.UserLogoutView.as_view() , name = 'logout'),
    path('register/', views.UserRegisterView.as_view() , name = 'register'),
    path('profile/<int:pk>', views.ProfileView.as_view() , name = 'profile'),
    path('edit/profile', views.EidtProfileView.as_view() , name = 'edit_profile'),

    path('follow/<int:pk>' , views.FollowView.as_view() , name ='follow'),
    path('unfollow/<int:pk>' , views.UnFollowView.as_view() , name ='unfollow'),

    path('password_reset/' , views.UserPasswordResetView.as_view() , name ='password_reset'),
    path('password_reset_done/' , views.UserPasswordResetDoneView.as_view() , name ='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>' , views.UserPasswordResetConfirmView.as_view() , name ='password_reset_confirm'),
    path('password_reset_complete/' , views.UserPasswordResetCompleteView.as_view() , name ='password_reset_complete'),

    path('api/' , include('account.api.urls'))

]
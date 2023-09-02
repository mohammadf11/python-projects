from django.urls import path
from . import views

app_name = 'send_email'

urlpatterns = [
    path('' , views.SendEmailView.as_view() , name = 'send_email')
]
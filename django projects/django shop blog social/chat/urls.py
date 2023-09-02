from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('<int:user_id>' , views.DirectMessageView.as_view() , name = 'direct_message'),
]
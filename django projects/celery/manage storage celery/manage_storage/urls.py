from django.urls import path
from . import views
app_name = 'storage'

urlpatterns = [
    path('' , views.Storage.as_view() , name ='storage'),
]
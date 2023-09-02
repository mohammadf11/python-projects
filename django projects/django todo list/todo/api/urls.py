from django.urls import path , include
from . import views 
from rest_framework import routers


router = routers.SimpleRouter()
router.register('', views.TodoViewSet , basename='api_todo')
urlpatterns = [
    # path('todo_list/' , views.TodoListCreateAPIView.as_view() , name = 'api_todo_list'),
    # path('todo_list/<int:pk>' , views.TodoRetrieveUpdateDestroyAPIView.as_view() , name = 'api_todo_list'),
    # path('register/' , views.UserRegisterApiView.as_view() , name = 'api_register'),
    path('todo/' , include(router.urls)),
    
]
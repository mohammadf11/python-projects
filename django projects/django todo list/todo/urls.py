from django.urls import path, include
from . import views

app_name = 'todo'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserRegistraionView.as_view(), name='register'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('', views.TodoListView.as_view(), name='todo_list'),
    path('create/', views.TodoCreateView.as_view(), name='todo_create'),
    path('update/<int:id>/', views.TodoUpdateView.as_view(), name='todo_update'),
    path('delete/<int:id>/', views.TodoDeleteView.as_view(), name='todo_delete'),



    path('api/', include('todo.api.urls'))
]

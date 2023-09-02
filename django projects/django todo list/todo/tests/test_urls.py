from django.test import TestCase
from django.urls import resolve , reverse
from .. import views
class TestTodoUrl(TestCase):
    
    def test_todo_login_url(self):
        url = reverse('todo:login')
        self.assertEquals(resolve(url).func.view_class , views.UserLoginView)

    def test_todo_register_url(self):
        url = reverse('todo:register')
        self.assertEquals(resolve(url).func.view_class , views.UserRegistraionView)

    def test_todo_logout_url(self):
        url = reverse('todo:logout')
        self.assertEquals(resolve(url).func.view_class , views.UserLogoutView)
    

    def test_todo_list_url(self):
        url = reverse('todo:todo_list')
        self.assertEquals(resolve(url).func.view_class , views.TodoListView)
    

    def test_todo_create_url(self):
        url = reverse('todo:todo_create')
        self.assertEquals(resolve(url).func.view_class , views.TodoCreateView)

    def test_todo_update_url(self):
        url = reverse('todo:todo_update' , args=[1])
        self.assertEquals(resolve(url).func.view_class , views.TodoUpdateView)

    def test_todo_delete_url(self):
        url = reverse('todo:todo_delete' , args=[1])
        self.assertEquals(resolve(url).func.view_class , views.TodoDeleteView)
    
    
    


        


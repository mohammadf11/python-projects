from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Todo

User = get_user_model()


class TestTodoModels(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username='reza',
            password='Ab12345!!'
        )
        Todo.objects.create(
            user = self.test_user,
            title='test1',
            description='test2',
            completed=False
        )
    
    def test_todo_on_delete_user_field(self):
        self.assertEqual(Todo.objects.count() , 1)
        self.test_user.delete()
        self.assertEqual(Todo.objects.count() , 0)

    def test_todo_max_length_title_field(self):
        todo1 = Todo.objects.get(id = 1)
        max_length_field = todo1._meta.get_field('title').max_length
        self.assertEqual(max_length_field , 100)

    
    def test_todo_default_completed_field(self):
        todo1 = Todo.objects.get(id = 1)
        default_field = todo1._meta.get_field('completed').default
        self.assertFalse(default_field)

    
    def test_todo_auto_now_add_created_field(self):
        todo1 = Todo.objects.get(id = 1)
        auto_now_add_field = todo1._meta.get_field('created').auto_now_add
        self.assertTrue(auto_now_add_field)

    def test_todo_auto_now_updated_field(self):
        todo1 = Todo.objects.get(id = 1)
        auto_now_field = todo1._meta.get_field('updated').auto_now
        self.assertTrue(auto_now_field)

    def test_todo_str_models(self):
        todo1 = Todo.objects.get(id = 1)
        self.assertEqual(str(todo1) , todo1.title)

        



from django.test import TestCase, Client
from django.urls import reverse, resolve
from .. import views
from django.contrib.auth import get_user_model
from .. models import Todo
from django.contrib.auth import login
from django.utils import timezone
from django.contrib.messages import get_messages

User = get_user_model()


def test_user():
    return User.objects.create_user(username='reza', password='Ab12345!!')


def user_info():
    return {
        "username": 'reza',
        "password": 'Ab12345!!'
    }


def test_todos(user=None):
    num_task = 10
    if user == None:
        user = User.objects.create_user(username='ali', password='Ab12345!!')
    for task_id in range(num_task):
        Todo.objects.create(
            user=user,
            title=f'title {"even" if task_id%2 == 0 else "odd"}',
            description=f'description {task_id}',
            completed=False if task_id % 2 == 0 else True
        )


class TestLoginView(TestCase):
    def setUp(self):
        self.login_url = reverse('todo:login')
        self.test_user = test_user()

    def test_todo_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/login.html')

    def test_todo_login_view_post_information_invalid(self):
        response = self.client.post(self.login_url, {})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/login.html')

    def test_todo_login_view_post_information_valid(self):
        response = self.client.post(self.login_url, user_info())

        self.assertRedirects(response, reverse(
            'todo:todo_list'), status_code=302)


class TestRegisterView(TestCase):
    def setUp(self) -> None:
        self.register_url = reverse('todo:register')
        self.template_name = 'todo/registration.html'

    def test_todo_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)

    def test_todo_register_view_post_information_invalid(self):
        response = self.client.post(self.register_url, {})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)

    def test_todo_register_view_post_information_valid(self):
        self.assertEquals(User.objects.count(), 0)
        response = self.client.post(self.register_url, {
            'username': 'alireza',
            'password1': 'Ab12345!!',
            'password2': 'Ab12345!!'
        })

        self.assertRedirects(response, reverse(
            'todo:todo_list'), status_code=302)
        self.assertEquals(User.objects.count(), 1)


class TestLogoutView(TestCase):
    def setUp(self) -> None:
        self.logout_url = reverse('todo:logout')

    def test_todo_logout_view(self):
        response = self.client.post(self.logout_url)
        self.assertRedirects(response, reverse(
            'todo:login') + f'?next={self.logout_url}', status_code=302)


class TestListTodo(TestCase):

    def setUp(self) -> None:
        self.todo_list_url = reverse('todo:todo_list')
        self.test_user = test_user()
        self.tempalte_name = 'todo/todo_list.html'
        test_todos(self.test_user)

    def test_todo_list_view_get_without_login(self):
        response = self.client.get(self.todo_list_url)
        self.assertRedirects(response, reverse(
            'todo:login') + f'?next={self.todo_list_url}', status_code=302)

    def test_todo_list_view_get_with_login_without_search(self):
        # response = self.client.post(self.login_url, {
        #     'username': 'reza',
        #     'password': 'Ab12345!!'
        # } ,follow=True)
        # print(response.context['request'])

        self.client.login(**user_info())
        response = self.client.get(self.todo_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.tempalte_name)
        self.assertEquals(len(response.context['tasks']), 10)
        self.assertEquals(len(response.context['tasks_complete']), 5)
        self.assertEquals(response.context['count'], 5)

    def test_todo_list_view_get_with_login_with_search(self):
        self.client.login(**user_info())
        response = self.client.get(self.todo_list_url + '?search-area= even')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.tempalte_name)
        self.assertEquals(len(response.context['tasks']), 5)
        self.assertEquals(len(response.context['tasks_complete']), 5)
        self.assertEquals(response.context['count'], 5)


class TestCreateTodoView(TestCase):
    def setUp(self) -> None:
        self.template_name = 'todo/todo_create.html'
        self.todo_create_url = reverse('todo:todo_create')
        self.user_test = test_user()
        test_todos(self.user_test)


    def test_todo_create_view_get_without_login(self):
        response = self.client.get(self.todo_create_url)
        self.assertRedirects(response,
                 reverse('todo:login') +f'?next={self.todo_create_url}', status_code=302)

    def test_todo_create_view_get_with_login(self):
        self.client.login(**user_info())
        response = self.client.get(self.todo_create_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)

    def test_todo_create_view_post_with_login_invalid(self):
        self.client.login(**user_info())
        response = self.client.post(self.todo_create_url, {})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Todo.objects.count(), 10)
        self.assertTemplateUsed(response,  self.template_name)

    def test_todo_create_view_post_with_login_valid(self):
        self.client.login(**user_info())
        response = self.client.post(self.todo_create_url,
                                    {
                                        'title': 'read book',
                                        'description': 'read book at 8:30',
                                        'completed': True,
                                    })
        self.assertRedirects(response, reverse(
            'todo:todo_list'), status_code=302)
        self.assertEquals(Todo.objects.count(), 11)
        self.assertTrue(Todo.objects.first().completed)


class TestUpdateTodo(TestCase):
    def setUp(self) -> None:
        self.user_test = test_user()
        test_todos(self.user_test)
        self.todo_update_url = reverse('todo:todo_update' , args=[10])
        self.template_name = 'todo/todo_update.html'

    
    def test_todo_update_view_get_without_login(self):
        response = self.client.get(self.todo_update_url)
        self.assertRedirects(response, reverse(
            'todo:login') + f'?next={self.todo_update_url}', status_code=302)

    def test_todo_update_view_get_with_login(self):
        self.client.login(**user_info())
        response = self.client.get(self.todo_update_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)

    def test_todo_update_view_post_with_login_invalid(self):
        self.client.login(**user_info())
        response = self.client.post(self.todo_update_url, {})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Todo.objects.count(), 10)
        self.assertTemplateUsed(response, self.template_name)

    def test_todo_update_view_post_with_login_valid(self):
        self.client.login(**user_info())
        self.assertTrue(Todo.objects.first().completed)
        self.assertEquals(Todo.objects.first().description, 'description 9')
        response = self.client.post(self.todo_update_url,
                                    {
                                        'title': 'update',
                                        'description': 'description 9 updated',
                                        'completed': False,
                                    })
        self.assertRedirects(response, reverse(
            'todo:todo_list'), status_code=302)
        self.assertEquals(Todo.objects.first().title, 'update')
        self.assertEquals(Todo.objects.first().description,
                          'description 9 updated')
        self.assertFalse(Todo.objects.first().completed)


        


class TestDeleteTodo(TestCase):

    def setUp(self) -> None:
        self.user_test = test_user()
        test_todos(self.user_test)
        self.todo_delete_url = reverse('todo:todo_delete' , args=[10])
        self.template_name = 'todo/todo_delete.html'

    def test_todo_delete_view_get_without_login(self):
        response = self.client.get(self.todo_delete_url)
        self.assertRedirects(response, reverse(
            'todo:login') + f'?next={self.todo_delete_url}', status_code=302)

    def test_todo_delete_view_get_with_login(self):
        self.client.login(**user_info())
        response = self.client.get(self.todo_delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)

    def test_todo_delete_view_post_with_login(self):
        self.assertTrue(Todo.objects.filter(id=10).exists())
        self.client.login(**user_info())
        response = self.client.post(self.todo_delete_url)
        self.assertFalse(Todo.objects.filter(id=10).exists())






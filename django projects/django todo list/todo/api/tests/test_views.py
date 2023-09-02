from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from ...models import Todo

User = get_user_model()


class BaseTestApi(APITestCase):
    def setUp(self) -> None:
        self.test_user = User.objects.create_user(
            username='ali',
            password='Ab12345!!'
        )

    def user_information(self):
        return {
            'username': 'ali',
            'password': 'Ab12345!!',
        }

    def authenticated(self):
        response = self.client.post(
            reverse('rest_login'), self.user_information())
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + response.data['access_token'])

    def other_user(self):
        User.objects.create_user(
            username='reza',
            password='Ab12345!!'
        )
        response = self.client.post(reverse('rest_login'), {
            'username': 'reza',
            'password': 'Ab12345!!'
        })
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + response.data['access_token'])

    def test_todos(self):
        num_task = 10
        for task_id in range(num_task):
            Todo.objects.create(
                user=self.test_user,
                title=f'title {"even" if task_id%2 == 0 else "odd"}',
                description=f'description {task_id}',
                completed=False if task_id % 2 == 0 else True
            )


class TestTodoListApiView(BaseTestApi):
    def setUp(self):
        super().setUp()
        self.url = reverse('todo:api_todo-list')

    def test_todo_list_view_without_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_todo_list_view_with_login(self):
        self.authenticated()
        self.test_todos()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 10)

    def test_todo_create_view_without_login(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 401)

    def test_todo_create_view_with_login_invalid_data(self):
        self.authenticated()
        response = self.client.post(self.url, {
            'title': 'test title todo',
        })
        self.assertEqual(response.status_code, 400)

    def test_todo_create_view_with_login_valid_data(self):
        self.authenticated()
        self.assertEqual(Todo.objects.count(), 0)
        response = self.client.post(self.url, {
            'title': 'test title todo',
            'description': 'test description todo',
            'completed': False,
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Todo.objects.count(), 1)
        self.assertEqual(response.data['title'], 'test title todo')
        self.assertEqual(response.data['description'], 'test description todo')
        self.assertFalse(response.data['completed'])


class TestTodoDeatailApiView(BaseTestApi):
    def setUp(self):
        super().setUp()
        self.test_todos()
        self.url = reverse('todo:api_todo-detail', args=[10])

    def test_todo_retrieve_get_withouth_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_todo_retrieve_view_with_login(self):
        self.authenticated()
        response = self.client.get(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'title odd')
        self.assertEqual(response.data['description'], 'description 9')
        self.assertTrue(response.data['completed'])

    def test_todo_update_view_without_login(self):
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, 401)

    def test_todo_update_view_other_user_not_access(self):
        self.other_user()
        response = self.client.patch(self.url, {})
        self.assertEqual(response.status_code, 403)

    def test_todo_update_view_owner_access(self):
        self.authenticated()
        self.assertEquals(Todo.objects.get(id=10).title, 'title odd')
        self.assertTrue(Todo.objects.get(id=10).completed)
        response = self.client.patch(self.url, {
            'title': 'update title',
            'completed': False
        })    
        self.assertEquals(Todo.objects.get(id=10).title, 'update title')
        self.assertFalse(Todo.objects.get(id=10).completed)


    def test_todo_delete_view_without_login(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 401)

    def test_todo_delete_view_other_user_not_access(self):
        self.other_user()
        response = self.client.patch(self.url, {})
        self.assertEqual(response.status_code, 403)

    def test_todo_update_view_owner_access(self):
        self.authenticated()
        self.assertEquals(Todo.objects.get(id=10).title, 'title odd')
        self.assertTrue(Todo.objects.get(id=10).completed)
        response1 = self.client.delete(self.url)
        response2 = self.client.delete(self.url)
        self.assertEqual(response1.status_code , 204)
        self.assertEqual(response2.status_code , 404)


    
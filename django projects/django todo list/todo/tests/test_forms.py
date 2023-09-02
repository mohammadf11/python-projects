from django.contrib.auth.forms import UserCreationForm
from django.test import TestCase
from ..forms import UserLoginForm
from django.contrib.auth import get_user_model
User = get_user_model()


class BaseTest(TestCase):
    def setUp(self) -> None:
        self.test_user = User.objects.create_user(username='reza', password='Ab12345!!')


class TestUserLoginForm(BaseTest):
    def test_todo_UserLoginForm_invalid(self):
        form = UserLoginForm(data={})
        username_error = form['username'].errors
        password_error = form['password'].errors

        self.assertFalse(form.is_valid())
        self.assertIn('This field is required.', username_error)
        self.assertIn('This field is required.', password_error)

    def test_todo_UserLoginForm_user_not_exist(self):
        form = UserLoginForm(data={
            'username': 'mohammad',
            'password': 'Ab12345!!'
        })

        username_error = form.non_field_errors()
        self.assertFalse(form.is_valid())
        self.assertIn('this user not found', username_error)

    def test_todo_UserLoginForm_valid(self):
        form = UserLoginForm(data={
            'username': 'reza',
            'password': 'Ab12345!!'

        })
        self.assertTrue(form.is_valid())

class TestUserCreationForm(BaseTest):
    def test_todo_UserCreationForm_user_exist_error(self):
        form = UserCreationForm(data={
            'username': 'reza',
            'password1': 'Ab12345!!',
            'password2': 'Ab12345!!'

        })
        errors = form.errors
        username_error = form['username'].errors

        self.assertFalse(form.is_valid())
        self.assertIn('A user with that username already exists.',errors['username'])
        self.assertIn('A user with that username already exists.', username_error)

    def test_todo_UserCreationForm_required_field(self):
        form = UserCreationForm(data={})

        username_error = form['username'].errors
        password1_error = form['password1'].errors
        password2_error = form['password2'].errors
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required.', username_error)
        self.assertIn('This field is required.', password1_error)
        self.assertIn('This field is required.', password2_error)

    def test_todo_UserCreationForm_password_didnt_match(self):
        form = UserCreationForm(data={
            'username': 'reza_test',
            'password1': 'Ab12345',
            'password2': 'Ab12345!!'
        })
        self.assertFalse(form.is_valid())
        password2_error = form['password2'].errors
        self.assertIn('The two password fields didn’t match.', password2_error)

    def test_todo_UserCreationForm_valid(self):
        form = UserCreationForm(data={
            'username': 'reza_test',
            'password1': 'Ab12345!!',
            'password2': 'Ab12345!!'

        })
        self.assertTrue(form.is_valid())





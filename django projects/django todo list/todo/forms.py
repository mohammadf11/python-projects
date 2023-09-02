from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control'}), required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('request')
        return super().__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username is not None and password:
            user = authenticate(
                self.request, username=username, password=password)
            if user is None:
                # raise ValidationError("this user not found")
                self.add_error(None, "this user not found") # non_filed_error
                # self.add_error('password', "this user not found") for filed

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User, Profile
from django.contrib.auth import authenticate


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password Confirm'}))

    class Meta:
        model = User
        fields = ('phone_number', 'email')
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('phone_number', 'email', 'password', 'is_active', 'is_admin')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)

        widgets = {
            'first_name': forms.TextInput(attrs={
                'id': "inputUsername",
                'placeholder': "Enter your first name"
                }),
            'last_name': forms.TextInput(attrs={
                'id': "inputLastName",
                'placeholder': "Enter your last name"
                }),
            
            'country': forms.TextInput(attrs={
                'id': "inputLastName",
                'placeholder': "Enter your country "
                }),
              
            'city': forms.TextInput(attrs={
                'id': "inputLastName",
                'placeholder': "Enter your city"
                }),

        }


class UserLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11 ,  widget=forms.TextInput(
        attrs={'placeholder': 'Phone Number'}))
    
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'password'}))
    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('request')
        return super().__init__(*args, **kwargs)

    def clean(self):
        phone_number = self.cleaned_data.get('phone_number')
        password = self.cleaned_data.get('password')
        if phone_number is not None and password:
            user = authenticate(
                self.request, phone_number=phone_number, password=password)
            if user is None:
                # raise ValidationError("this user not found")
                self.add_error(None, "this user not found") # non_filed_error
                # self.add_error('password', "this user not found") for file

from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()


class ReviewForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=True)
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}), required=True)
    review = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control'}), required=True)



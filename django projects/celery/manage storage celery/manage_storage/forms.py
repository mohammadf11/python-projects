from django import forms


class ImageForm(forms.Form):
    path = forms.CharField(label='Enter path file for upload',widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=False)

    object_name_delete = forms.CharField(label='Enter object name for delete', widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=False)

    object_name_download = forms.CharField(label='Enter object name for download', widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=False)
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import ImageForm
from .tasks import upload_object_task, delete_object_task , download_object_task
from .bucket import bucket
from PIL import Image

# Create your views here.


class Storage(FormView):
    template_name = 'index.html'
    form_class = ImageForm
    success_url = reverse_lazy('storage:storage')

    def form_valid(self, form):
        path = form.cleaned_data.get('path')
        object_name_for_delete = form.cleaned_data.get('object_name_delete')
        object_name_download = form.cleaned_data.get('object_name_download')
        object_name_for_upload = path.split('/')[-1]
        upload_object_task.delay(path, object_name_for_upload)
        delete_object_task.delay(object_name_for_delete)
        download_object_task.delay(object_name_download)

        return super().form_valid(form)

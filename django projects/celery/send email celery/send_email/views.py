from django.shortcuts import render
from django.views.generic import FormView
from .forms import ReviewForm
from django.http import HttpResponse
from .tasks import send_email_task ,send_email

# Create your views here.


class SendEmailView(FormView):
    template_name = 'index.html'
    form_class = ReviewForm

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        review = form.cleaned_data.get('review')
        send_email_task.delay(name, email, review)
        # send_email(name, email, review)
        msg = "Thanks for the review!"
        return HttpResponse(msg)

    

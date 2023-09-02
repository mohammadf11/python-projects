from django.shortcuts import render
from django.contrib.auth.views import LoginView , LogoutView
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.views.generic import ListView
from blog.models import Article
from django.contrib.auth import authenticate, login
from .forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import SuperuserAuthorAccessMixins  
# Create your views here.


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
        
        


class UserRegisterView(FormView):
    form_class = UserCreationForm
    template_name = 'accounts/registration.html'
    success_url = reverse_lazy('blog:article_list')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request , user , backend='django.contrib.auth.backends.ModelBackend')
        return super().form_valid(form)

class UserLogoutView(LoginRequiredMixin  , LogoutView):
    pass

class UserProfileView(LoginRequiredMixin ,SuperuserAuthorAccessMixins , ListView):
    template_name = 'accounts/profile.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(author = self.request.user)

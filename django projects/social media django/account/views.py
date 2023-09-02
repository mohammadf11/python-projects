from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, FormView, UpdateView, DetailView, View
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import View

from .forms import ProfileForm, UserLoginForm, UserCreationForm
from .models import User, Profile
from social_media.models import Post

from django.contrib.auth import authenticate, login

from django.contrib.auth.views import (LogoutView, PasswordResetView, PasswordResetDoneView,
                                       PasswordResetConfirmView, PasswordResetCompleteView,
                                       LoginView)


from social_media.models import Follow

from django.contrib.auth.mixins import LoginRequiredMixin
from . import mixins
# Create your views here.


class UserLoginView(mixins.LogoutRequirementMixin, LoginView):
    # form_class = UserLoginForm
    template_name = 'account/login.html'

    # def form_valid(self, form):
    #     phone_number = form.cleaned_data['phone_number']
    #     password = form.cleaned_data['password']
    #     user = authenticate(phone_number=phone_number, password=password)
    #     if user is not None:
    #         login(self.request, user)
    #     else:
    #         return render(self.request , self.template_name , {'form':self.form_class()})
    #     return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse_lazy('account:profile', args=(self.request.user.id,))


class UserLogoutView(LoginRequiredMixin, LogoutView):
    pass


class UserRegisterView(mixins.LogoutRequirementMixin, FormView):

    form_class = UserCreationForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('social_media:home')

    def form_valid(self, form):
        phone_number = form.cleaned_data['phone_number']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password2']
        user = User.objects.create_user(phone_number=phone_number,
                                 email=email, password=password)
        login(self.request , user ) 
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'account/profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        print(self.request.user.id)
        context = super().get_context_data()
        context['profile'] = context['user'].profile
        context['posts'] = Post.objects.filter(user=context['user'])
        context['is_follow'] = Follow.objects.filter(
            follower=self.request.user, following=context['user']).exists()

        return context


class EidtProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'account/edit_profile.html'

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('account:profile', args=(self.request.user.id,))


class FollowView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        follower = request.user
        following = User.objects.get(id=kwargs['pk'])
        Follow.objects.create(follower=follower, following=following)
        return redirect('account:profile', following.id)


class UnFollowView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        follower = request.user
        following = User.objects.get(id=kwargs['pk'])
        Follow.objects.get(follower=follower, following=following).delete()
        return redirect('account:profile', following.id)


class UserPasswordResetView(PasswordResetView):
    template_name = 'account/password_reset.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password_reset_email.html'


class UserPasswordResetDoneView(PasswordResetView, PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'

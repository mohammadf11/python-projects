from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.views import (LoginView, LogoutView, PasswordResetView, PasswordResetDoneView,
                                       PasswordResetConfirmView, PasswordResetCompleteView)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView, FormView, UpdateView, DetailView, View
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from random import randint

from . import mixins
from .forms import ProfileForm, UserLoginForm, UserCreationForm, UserVerfiyCodeForm
from .models import User, Profile, VerifyCode
from social_media.models import Post
from social_media.models import Follow


# Create your views here.


# class UserLoginView(mixins.LogoutRequirementMixin, FormView):
#     form_class = UserLoginForm
#     template_name = 'account/login.html'

#     def form_valid(self, form):
#         phone_number = form.cleaned_data['phone_number']
#         password = form.cleaned_data['password']
#         user = authenticate(phone_number=phone_number, password=password)
#         if user is not None:
#             login(self.request, user)
#         else:
#             return render(self.request , self.template_name , {'form':self.form_class(self.request.POST)})
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse_lazy('account:profile', args=(self.request.user.id,))

class UserLoginView(mixins.LogoutRequirementMixin, LoginView):
    template_name = 'account/login.html'

    def get_success_url(self):
        return reverse_lazy('account:profile', args=(self.request.user.id,))


class UserLogoutView(LoginRequiredMixin, LogoutView):
    pass


class UserRegisterView(mixins.LogoutRequirementMixin, FormView):

    form_class = UserCreationForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('account:verify_code')

    def form_valid(self, form):
        data = form.cleaned_data
        self.request.session['user_info'] = {
            'phone_number': data['phone_number'],
            'email': data['email'],
            'password': data['password2'],
        }
        code = randint(10000, 99999)

        VerifyCode.objects.filter(phone_number=data['phone_number']).delete()
        VerifyCode.objects.create(phone_number=data['phone_number'], code=code)
        return super().form_valid(form)


class UserVerifyCodeView(View):
    template_name = 'account/verify_code.html'
    form_class = UserVerfiyCodeForm

    def get(self, request):
        verify_code = VerifyCode.objects.get(
            phone_number=request.session['user_info']['phone_number'])
        return render(request, self.template_name, {'form': self.form_class , 'verify_code' : verify_code})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user_info = request.session['user_info']
            verify_code_instance = VerifyCode.objects.get(
                phone_number=user_info['phone_number'])

            if verify_code_instance.code == data['code']:
                user = User.objects.create_user(
                    phone_number=user_info['phone_number'],
                    email=user_info['email'],
                    password=user_info['password'],
                )
                login(request, user)
                VerifyCode.objects.filter(
                    phone_number=user_info['phone_number']).delete()
                return redirect('shop:product_list')
            else:
                return redirect('account:verify_code')
        return render(request, self.template_name, {'form': form})


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'account/profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profile'] = context['user'].profile
        context['posts'] = Post.objects.filter(user=context['user'])
        context['is_access'] = self.request.user.is_staff or context['profile'].id == self.request.user.profile.id
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

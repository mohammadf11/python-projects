from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, View
from django.db.models import Q

from .models import Post, Like
from . import mixins

# Create your views here.


class PostListView(ListView):
    template_name = 'social_media/post_list.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        posts = Post.objects.all()
        search_input = self.request.GET.get('search_area')
        if search_input:
            posts = posts.filter(
                Q(title__contains=search_input) | Q(body__contains=search_input)
            )
        return posts



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ('title', 'body', 'image')
    template_name = 'social_media/post_create.html'
    success_url = reverse_lazy('social_media:post_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin ,mixins.IsStaffOrOwnerModifiedPostMixin, UpdateView):
    model = Post
    fields = ('title', 'body', 'image')
    template_name = 'social_media/post_update.html'
    success_url = reverse_lazy('social_media:post_list')


class PostDeleteView(LoginRequiredMixin , mixins.IsStaffOrOwnerModifiedPostMixin, DeleteView):
    model = Post
    template_name = 'social_media/post_delete.html'
    context_object_name = 'post'

    def get_success_url(self):
        return reverse_lazy('social_media:post_list')


class LikePostView(LoginRequiredMixin, mixins.OneLikeMixin, View):
    def get(self, request, *arg, **kwargs):
        user = request.user
        post = Post.objects.get(id=kwargs['pk'])
        Like.objects.create(user=user, post=post)
        return redirect('social_media:post_list')


class DisLikePostView(LoginRequiredMixin,View):
    def get(self, request, *arg, **kwargs):
        user = request.user
        post = Post.objects.get(id=kwargs['pk'])
        like = get_object_or_404(Like, user=user, post=post)
        like.delete()
        return redirect('social_media:post_list')

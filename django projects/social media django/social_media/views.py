from django.shortcuts import render , redirect , get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, View

from .models import Post, Like
from django.contrib.auth.mixins import LoginRequiredMixin
from . import mixins
from django.db.models import Q


# Create your views here.


class Home(ListView):
    template_name = 'social_media/home.html'
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


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    fields = ('title', 'body', 'image')
    template_name = 'social_media/create_post.html'
    success_url = reverse_lazy('social_media:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdatePost(mixins.ModifiedPostMixin, UpdateView):
    model = Post
    fields = ('title', 'body', 'image')
    template_name = 'social_media/update_post.html'
    success_url = reverse_lazy('social_media:home')


class DeletePost(mixins.ModifiedPostMixin, DeleteView):
    model = Post
    template_name = 'social_media/post_confirm_delete.html'
    context_object_name = 'post'

    def get_success_url(self):
        return reverse_lazy('social_media:home')


class LikePost(LoginRequiredMixin , mixins.OneLikeMixin,View):
    def get(self, request, *arg, **kwargs):
        user = request.user
        post = Post.objects.get(id=kwargs['pk'])
        Like.objects.create(user=user, post=post)
        return redirect('social_media:home')



class DisLikePost(View):
    def get(self, request, *arg, **kwargs):
        user = request.user
        post = Post.objects.get(id=kwargs['pk'])
        like =get_object_or_404(Like, user=user, post=post)
        like.delete()
        return redirect('social_media:home')


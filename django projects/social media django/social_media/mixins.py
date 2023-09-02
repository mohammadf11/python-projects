from .models import Post
from django.shortcuts import redirect
from  .models import Post , Like


class ModifiedPostMixin():
    def dispatch(self, request, *args, **kwargs):
        user_post = Post.objects.get(id=kwargs['pk']).user
        if user_post == request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("social_media:home")

class OneLikeMixin():
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        post = Post.objects.get(id=kwargs['pk'])
        if not Like.objects.filter(user = user , post = post).exists():
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('social_media:home')

    


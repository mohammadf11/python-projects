from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models import Article
from . import mixins


# from blog.test.fake_objects import ArticleCategoryFactory , ArticleFactory ,UserFactory
# from .models import ArticleCategory
# admin_user = UserFactory(is_admin = True)
# categories = [ArticleCategoryFactory() for _ in range(5)]
# for id in range(20):
#     ArticleFactory(
#         author=admin_user,
#         category=ArticleCategory.objects.get(id=(id % 5) + 1)
#     )


# Create your views here.
class ArticleLsitView(ListView):
    template_name = 'blog/article_lsit.html'
    context_object_name = 'articles'
    paginate_by = 6

    def get_queryset(self):
        Articles =  Article.objects.published()
        search_input = self.request.GET.get('search_area')
        if search_input:
            Articles = Articles.filter(
                Q(title__contains=search_input) | Q(description__contains=search_input)
            )
        return Articles


class ArticleDetailView(DetailView):
    queryset = Article.objects.published()
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'


class ArticleCreatelView(LoginRequiredMixin, mixins.IsStaffAccessMixins, CreateView):
    model = Article
    fields = ('category', 'title', 'description', 'image', 'is_publish')
    template_name = 'blog/article_create.html'
    success_url = reverse_lazy('blog:manage_article')
    
    def form_valid(self, form):
        form.instance.author  = self.request.user
        return super().form_valid(form)


class ArticleUpdatelView(LoginRequiredMixin, mixins.IsSuperuserOrOwnerAccessMixins,UpdateView):
    model = Article
    fields = ('category', 'title', 'description', 'image', 'is_publish')
    template_name = 'blog/article_update.html'
    success_url = reverse_lazy('blog:manage_article')


class ArticleDeletelView(LoginRequiredMixin, mixins.IsSuperuserOrOwnerAccessMixins,DeleteView):
    model = Article
    template_name = 'blog/article_delete.html'
    success_url = reverse_lazy('blog:manage_article')


class ManageArticleView(LoginRequiredMixin, mixins.IsStaffAccessMixins,View):
    template_name = 'blog/manage_article.html'
    def get(self , request):
        if request.user.is_superuser:
            articles = Article.objects.all()
        else:
            articles = Article.objects.filter(author=request.user)
        return render(request, self.template_name , {'articles':articles})

    

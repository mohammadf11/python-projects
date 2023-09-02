from django.shortcuts import render , get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Article, Category
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from .mixins import CategoryCountMixins ,ArticlePublishMixins , ArticleUpdateMixins
from account.mixins import  SuperuserAuthorAccessMixins , SuperuserAccessMixins 
from django.db.models import Q

# Create your views here.


class ListArticleView(ListView):
    template_name = 'blog/article_list.html'
    context_object_name = 'articles'
    paginate_by = 3

    def get_queryset(self):
        articles = Article.objects.publish()
        search_input = self.request.GET.get('search-area') or ''    
        if search_input :
            articles = articles.filter(
                Q(title__contains=search_input) | Q(body__contains=search_input) | Q(category__name__contains=search_input)) 
        return articles

class CategoryListArticleView(CategoryCountMixins , ListView):
    template_name = 'blog/catrgory_list_article.html'
    context_object_name = 'articles'
    paginate_by = 2

    def setup(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category.objects.active() , slug = kwargs.get('category_slug'))
        super().setup(request, *args, **kwargs)

    def get_queryset(self):
        return self.category.articles.publish()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category 
        return context


class DetailArticleView(ArticlePublishMixins , DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'


class CreateArticleView(SuperuserAuthorAccessMixins,CreateView):
    model = Article
    fields = ['category', 'title', 'body', 'image', 'is_complete']
    template_name = 'blog/create_update_article.html'
    success_url = reverse_lazy('blog:article_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.body[:20])
        if form.instance.is_complete == True:
            form.instance.status = 'lock'

        return super().form_valid(form)


class UpdateArticleView(SuperuserAuthorAccessMixins , ArticleUpdateMixins , UpdateView):
    model = Article
    fields = ['category', 'title', 'body', 'image', 'is_complete']
    template_name = 'blog/create_update_article.html'
    success_url = reverse_lazy('blog:article_list')

    def form_valid(self, form):
        if form.instance.is_complete == True:
            form.instance.status = 'lock'
        else:
            form.instance.status = 'draft'
        return super().form_valid(form)


class DeleteArticleView(SuperuserAccessMixins ,DeleteView):
    model = Article
    template_name = 'blog/delete_article.html'
    context_object_name = 'article'
    success_url = reverse_lazy('blog:article_list')

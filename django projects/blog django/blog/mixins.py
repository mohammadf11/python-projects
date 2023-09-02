from django.shortcuts import get_object_or_404, redirect
from .models import Article, Category
from django.core.exceptions import PermissionDenied


class CategoryCountMixins:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            category = get_object_or_404(
                Category.objects.active(), slug=self.kwargs.get('category_slug'))
            if category.articles.publish().count() == 0:
                return redirect('blog:article_list')
        return super().dispatch(request, *args, **kwargs)


class ArticlePublishMixins:
    def dispatch(self, request, *args, **kwargs):
        article = Article.objects.publish().filter(pk=self.kwargs.get('pk'))
        if not(request.user.is_superuser or (article.author == request.user)):
            article = article.exists()
            if not article:
                return redirect('blog:article_list')
        return super().dispatch(request, *args, **kwargs)

class ArticleUpdateMixins:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            article = get_object_or_404(Article, id=self.kwargs.get('pk'))
            if article.status in ['lock', 'publish']:
                raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

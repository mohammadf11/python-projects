from django.test import TestCase
from django.urls import reverse , resolve
from .. import views


class  TestBlogUrl(TestCase):
    def test_blog_article_list_url(self):
        url = reverse('blog:article_list')
        self.assertEqual(resolve(url).func.view_class , views.ListArticleView )

    
    def test_blog_category_list_article_url(self):
        url = reverse('blog:category_list_article' , args=['slug'])
        self.assertEqual(resolve(url).func.view_class , views.CategoryListArticleView )

    def test_blog_article_detail_url(self):
        url = reverse('blog:article_detail' , args=[1])
        self.assertEqual(resolve(url).func.view_class , views.DetailArticleView )

    def test_blog_create_article_url(self):
        url = reverse('blog:create_article')
        self.assertEqual(resolve(url).func.view_class , views.CreateArticleView )

    def test_blog_update_article_url(self):
        url = reverse('blog:update_article' , args=[1])
        self.assertEqual(resolve(url).func.view_class , views.UpdateArticleView )

    def test_blog_delete_article_url(self):
        url = reverse('blog:delete_article', args=[1])
        self.assertEqual(resolve(url).func.view_class , views.DeleteArticleView )
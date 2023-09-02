from django.db import models
from account.models import User

# Create your models here.
class ArticleManager(models.Manager):
    def published(self):
        return self.filter(is_publish = True)

class ArticleCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    is_active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
        
    class Meta:
        ordering = ['is_active']
        verbose_name = 'ArticleCategory'
        verbose_name_plural = 'ArticleCategories'


class Article(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE , related_name='articles')
    category = models.ForeignKey(ArticleCategory, on_delete = models.CASCADE , related_name='Articles')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to = 'image_blog/')
    is_publish = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    objects = ArticleManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']
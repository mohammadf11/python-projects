from django.db import models
from account.models import User
from django.urls import reverse

# manager


class ArticleManger(models.Manager):
    def publish(self):
        return self.filter(status='publish')


class CategoryManger(models.Manager):
    def active(self):
        return self.filter(is_active=True)


# model

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CategoryManger()

    def __str__(self):
        return self.name


    class Meta:
        verbose_name_plural = 'categories'
        verbose_name = 'category'

    def get_absolute_url(self):
        return reverse('blog:category_list_article', kwargs={'category_slug': self.slug})


class Article(models.Model):
    STATUS_CHOICES = (
        ("publish", "Publish"),
        ("draft", "Draft"),
        ("back", "Back"),
        ("lock", "Lock"),

    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    body = models.TextField()
    image = models.ImageField(upload_to = 'images/' , blank = True , null = True )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')
    is_complete = models.BooleanField(
        default=False, verbose_name='Send to admin')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ArticleManger()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:article_detail', kwargs={'pk': self.id})

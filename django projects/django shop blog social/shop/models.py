from django.db import models

# Create your models here.
class ShopManager(models.Manager):
    def availabled(self):
        return self.filter(is_available = True)

class ShopCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    is_active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-is_active']
        verbose_name = 'ShopCategory'
        verbose_name_plural = 'ShopCategories'

class Product(models.Model):
    category = models.ForeignKey(ShopCategory, on_delete = models.CASCADE , related_name='products')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to = 'image_shop/')
    price = models.IntegerField()
    is_available = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    objects = ShopManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']
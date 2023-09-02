from django.contrib import admin
from .models import ArticleCategory , Article

# Register your models here.

@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_editable = ['is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_publish']
    list_editable = ['is_publish']
    list_filter = ['is_publish']
    raw_id_fields = ['category']
    search_fields = ['title', 'is_publish']
    prepopulated_fields = {'slug': ('title',)}


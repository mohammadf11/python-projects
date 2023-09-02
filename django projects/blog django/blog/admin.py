from django.contrib import admin
from .models import Article , Category

# Register your models here.
@admin.action()
def make_published(modeladmin, request, queryset):
    queryset.update(status='publish')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status')
    list_filter = ('status','category')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author','category')
    date_hierarchy = 'created'
    ordering = ('status', 'created')
    actions = [make_published]

    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    


from django.contrib import admin
from .models import Post, Follow, Like
# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', )
    list_editable = ('title',)
    search_fields = ('title' , )



admin.site.register(Follow)
admin.site.register(Like)

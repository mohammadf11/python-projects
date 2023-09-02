from django.contrib import admin
from .models import Todo
# Register your models here.
@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['user','title','completed']
    list_editable = ['title' , 'completed']
    search_fields = ['title' , 'description']
    raw_id_fields = ['user']
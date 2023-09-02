from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.ListArticleView.as_view(), name='article_list'),
    path('category_list_article/<slug:category_slug>', views.CategoryListArticleView.as_view(), name='category_list_article'),
    path('article_detail/<int:pk>/', views.DetailArticleView.as_view(), name='article_detail'),
    
    path('create_article' , views.CreateArticleView.as_view() , name = 'create_article'),
    path('update_article/<int:pk>' , views.UpdateArticleView.as_view() , name = 'update_article'),
    path('delete_article/<int:pk>' , views.DeleteArticleView.as_view() , name = 'delete_article'),
]
    
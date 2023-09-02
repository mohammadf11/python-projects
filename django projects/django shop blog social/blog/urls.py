from django.urls import path , include
from rest_framework import routers
from . import views
from . import apis

app_name = 'blog'

urlpatterns = [
    path('article_list/', views.ArticleLsitView.as_view(), name='article_list'),
    path('article_detail/<int:pk>/',
         views.ArticleDetailView.as_view(), name='article_detail'),
    path('article_create/', views.ArticleCreatelView.as_view(),
         name='article_create'),
    path('article_update/<int:pk>/', views.ArticleUpdatelView.as_view(),
         name='article_update'),
    path('article_delete/<int:pk>/', views.ArticleDeletelView.as_view(),
         name='article_delete'),
    path('manage_article/', views.ManageArticleView.as_view(), name='manage_article'),
]

# api urls
router = routers.SimpleRouter()
router.register('articles', apis.ArticleModelViewSet , basename='api_article')
router.register('article_categories', apis.ArticleCategoryModelViewSet , basename='api_article_categories')
urlpatterns += [
    path('api/' , include(router.urls)),
]

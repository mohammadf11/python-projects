from rest_framework import serializers
from .models import Article , ArticleCategory

class CreateArticleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Article
        exclude = ('author',)

class ArticleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class ArticleCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = '__all__'
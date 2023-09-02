from rest_framework import serializers
from .models import Post, Like, Follow


class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ('user',)

class StaffPostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class LikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('post',)


class StaffLikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('user', 'post')


class FollowSerializers(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('following',)


class StaffFollowSerializers(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('follower','following')
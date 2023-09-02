from django.db import models
from account.models import User
from mdeditor.fields import MDTextField

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE , related_name='posts')
    title = models.CharField(max_length=100)
    body = MDTextField()
    image = models.ImageField(upload_to = 'image_post/')
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now= True)

    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']
        

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete = models.CASCADE ,related_name='follower' )
    following = models.ForeignKey(User, on_delete = models.CASCADE , related_name='following' )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} follow {}'.format(self.follower , self.following)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE , related_name='user_likes')
    post = models.ForeignKey(Post, on_delete = models.CASCADE , related_name='post_likes')
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '{} like {}'.format(self.user , self.post.title)


from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin
from .managers import UserManager
from mdeditor.fields import MDTextField


class User(AbstractBaseUser , PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address', max_length=255, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def is_like_post(self , post_id):
        from social_media.models import Like , Post
        post = Post.objects.get(id = post_id)
        if Like.objects.filter(user = self , post = post).exists():
            return True
        return False
        

class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to='image_profile/', null=True, blank=True)
    about = MDTextField(null=True, blank=True)

    def __str__(self):
        # return '{} {}'.format(self.first_name, self.last_name)
        return str(self.id)

    def get_first_name(self):
        if self.first_name is None:
            return ''
        return self.first_name

    def get_last_name(self):
        if self.last_name == None:
            return ''
        return self.last_name
    
    def get_city(self):
        if self.city == None:
            return ''
        return self.city
        
    def get_country(self):
        if self.country == None:
            return ''
        return self.country
        
    def get_full_name(self):
        return '{} {}'.format(self.get_first_name(), self.get_last_name())

    def is_full_name(self):
        return  len(self.get_first_name() + self.get_last_name())
            




class VerifyCode(models.Model):
    phone_number = models.CharField(max_length=11)
    code = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.code)
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User , Profile



@receiver(post_save, sender=User)
def profile_save(sender , **kwargs):
    if kwargs['created']:
        Profile.objects.create(user = kwargs['instance'])
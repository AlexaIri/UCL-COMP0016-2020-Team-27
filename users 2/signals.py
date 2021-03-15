from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created: # if the user account was created
        Profile.objects.create(user=instance) # create a profile of the instance of that user
        
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
   
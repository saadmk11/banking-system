from django.db.models.signals import post_save
from .models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_profile, sender=User)


def save_profile(sender, instance, created, **kwargs):
    instance.profile.save()

post_save.connect(save_profile, sender=User)
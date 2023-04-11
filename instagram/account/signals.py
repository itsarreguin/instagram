# Python standard library
from typing import Any
from typing import Dict

# Django imports
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Model

# Instagram models
from instagram.account.models import User
from instagram.account.models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender: Model, instance: User, created: User, **kwargs: Dict[str, Any]):
    """ create user profile
    Save a profile after than new user has been created
    """

    if created:
        profile = Profile.objects.create(user=instance)
    else:
        try:
            profile = Profile.objects.get(user=instance)
            profile.save()
        except:
            Profile.objects.create(user=instance)
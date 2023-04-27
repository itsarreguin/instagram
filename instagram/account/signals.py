# Python standard library
from typing import Any
from typing import Dict

# Django dispatch
from django.dispatch import receiver
# Django database
from django.db.models.signals import post_save

# Instagram models
from instagram.account.models import User
from instagram.account.models import Profile
from instagram.posts.models import Collection


@receiver(post_save, sender=User)
def create_user_profile(instance: User, created: User, **kwargs: Dict[str, Any]) -> None:
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


@receiver(post_save, sender=User)
def create_default_collection(instance: User, created: User, **kwargs: Dict[str, Any]) -> None:
    """ Save a default collection after create new user """
    if created:
        Collection.objects.create(user=instance, name='default')
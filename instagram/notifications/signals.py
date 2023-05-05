# Python standard library
from typing import Any
from typing import Dict

# Django dispatch
from django.dispatch import receiver
# Django database
from django.db.models.signals import post_save
# Django utils
from django.utils.crypto import get_random_string

# Instagram models
from instagram.notifications.models import Notification


@receiver(post_save, sender=Notification)
def collection_slug(instance: Notification, **kwargs: Dict[str, Any]) -> None:
    """ Save unique slug for each notification """
    
    if not instance.slug:
        instance.slug = get_random_string(length=6)
        instance.save()
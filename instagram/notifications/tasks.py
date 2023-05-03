# Python standard library
from typing import Any
from typing import Dict
from typing import Type

# Django database
from django.db.models import Model

# Instagram celery
from instagram import celery
# Instagram models
from instagram.account.models import User
from instagram.notifications.models import Notification


@celery.task(max_retries=4)
def send_notification(**kwargs: Dict[str, Any]) -> Type[Model]:
    receiver_username: str = kwargs['receiver_username']
    sender_username: str = kwargs['sender_username']
    try:
        receiver = User.objects.filter(username=receiver_username).first()
        sender = User.objects.filter(username=sender_username).first()
    except (User.DoesNotExist, TypeError, OverflowError):
        receiver = None
        sender = None
    
    new_notification = Notification.objects.create(
        receiver=receiver,
        sender=sender,
        category=kwargs['category'],
        object_id=kwargs['object_id'],
        object_slug=kwargs['object_slug']
    )
    return new_notification
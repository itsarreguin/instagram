# Python standard library
from typing import Dict
from typing import List

# Django HTTP package
from django.http import HttpRequest
# Django database
from django.db.models import Model

# Instagram models
from instagram.notifications.models import Notification


def notifications(request: HttpRequest) -> Dict[str, List[Model]]:
    if request.user.is_authenticated:
        notifications_list = (
            Notification.objects
            .filter(receiver=request.user)
            .order_by('-created').all()
        )
        return { 'notifications': notifications_list }
    
    return { 'notifications': [] }


def readed_notifications(request: HttpRequest) -> Dict[str, List[Model]]:
    if request.user.is_authenticated:
        readed_notifications_list = (
            request.user.notifications.filter(is_read=False).count()
        )
        return { 'notifications_counter': readed_notifications_list }
    
    return { 'notifications_counter': [] }
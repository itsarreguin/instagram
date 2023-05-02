# Python standard library
from typing import Dict

# Django HTTP package
from django.http import HttpRequest
# Django database
from django.db.models import Model

# Instagram models
from instagram.notifications.models import Notification


def notifications(request: HttpRequest) -> Dict[str, Model] | None:
    if request.user.is_authenticated:
        notifications_list = (
            Notification.objects.filter(receiver=request.user).all()
        )
        return { 'notifications': notifications_list }
    
    return {}
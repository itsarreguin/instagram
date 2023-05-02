# Python standard library
from typing import List

# Django imports
from django.urls import path

# Instagram views
from instagram.notifications.views import NotificationsView


app_name: str = 'notifications'

urlpatterns: List[path] = [
    path(
        route='notifications/',
        view=NotificationsView.as_view(),
        name='all'
    ),
]
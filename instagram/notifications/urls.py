# Python standard library
from typing import List

# Django imports
from django.urls import path

# Instagram views
from instagram.notifications.views import NotificationsView
from instagram.notifications.views import NotificationDeleteView


app_name: str = 'notifications'

urlpatterns: List[path] = [
    path(
        route='notifications/',
        view=NotificationsView.as_view(),
        name='all'
    ),
    path(
        route='notifications/<int:pk>/delete',
        view=NotificationDeleteView.as_view(),
        name='delete'
    ),
]
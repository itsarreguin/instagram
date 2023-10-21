# Python standard library
from typing import List

# Django urls
from django.urls import path

# Instagram views
from instagram.messenger.views import MessengerView
from instagram.messenger.views import InboxDetailView


app_name: str = 'messenger'

urlpatterns: List[path] = [
    path('messages/', MessengerView.as_view(), name='home'),
    path(
        route='messages/<uuid:uuid>/',
        view=InboxDetailView.as_view(),
        name='inbox'
    ),
]
# Python standard library
from typing import List

# Django urls
from django.urls import path

# Instagram views
from instagram.messenger.views import MessengerView


app_name: str = 'messenger'

urlpatterns: List[path] = [
    path('messages/', MessengerView.as_view(), name='home'),
]
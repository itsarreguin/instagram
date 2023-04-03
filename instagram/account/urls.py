# Python stantad library
from typing import List

# Django imports
from django.urls import path

# instagram account views
from instagram.account.views.users import feed
from instagram.account.views.auth import LoginView
from instagram.account.views.auth import LogoutView


app_name: str = 'account'

urlpatterns: List[path] = [
    
    path('', feed, name='feed'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]
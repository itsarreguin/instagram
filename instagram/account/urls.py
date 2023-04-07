# Python stantad library
from typing import List

# Django imports
from django.urls import path

# instagram account views
from instagram.account.views.users import feed
from instagram.account.views.users import ProfileView
from instagram.account.views.auth import LoginView
from instagram.account.views.auth import SignUpView
from instagram.account.views.auth import LogoutView


app_name: str = 'account'

urlpatterns: List[path] = [
    
    path(
        route = 'login/',
        view = LoginView.as_view(),
        name = 'login'
    ),
    path(
        route = 'signup/',
        view = SignUpView.as_view(),
        name = 'signup'
    ),
    path(
        route = 'logout/',
        view = LogoutView.as_view(),
        name = 'logout'
    ),
    path(
        route = '',
        view = feed,
        name = 'feed'
    ),
    path(
        route = '<str:username>/',
        view = ProfileView.as_view(),
        name = 'profile'
    ),
]
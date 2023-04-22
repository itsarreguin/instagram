# Python stantad library
from typing import List

# Django imports
from django.urls import path

# Instagram account auth views
from instagram.account.views.auth import LoginView
from instagram.account.views.auth import SignUpView
from instagram.account.views.auth import LogoutView
from instagram.account.views.auth import PasswordResetRequestView
from instagram.account.views.auth import PasswordResetView
# Instagram account user views
from instagram.account.views.users import FeedView
from instagram.account.views.users import ProfileView
from instagram.account.views.users import EditProfileView
from instagram.account.views.users import EditAccountView
from instagram.account.views.users import ChangePasswordView


app_name: str = 'account'

urlpatterns: List[path] = [
    
    path('login/', view=LoginView.as_view(), name='login' ),
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
        route = 'password/reset/',
        view = PasswordResetRequestView.as_view(),
        name = 'password-reset-request'
    ),
    path(
        route = 'password/reset/<uidb64>/<str:token>/',
        view = PasswordResetView.as_view(),
        name = 'password-reset'
    ),
    path('', view=FeedView.as_view(), name='feed'),
    path(
        route = '<str:username>/',
        view = ProfileView.as_view(),
        name = 'profile'
    ),
    path(
        route = 'settings/profile/',
        view = EditProfileView.as_view(),
        name = 'edit-profile'
    ),
    path(
        route = 'settings/account/',
        view = EditAccountView.as_view(),
        name = 'edit-account'
    ),
    path(
        route = 'settings/password/change/',
        view = ChangePasswordView.as_view(),
        name = 'change-password'
    ),
]
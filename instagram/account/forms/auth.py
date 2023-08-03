# Django imports
from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import ValidationError

# Instagram models
from instagram.account.models import User


class LoginForm(forms.Form):

    username = forms.CharField(
        max_length=30, min_length=4,
        widget=forms.TextInput(attrs={ 'class': 'input-auth' })
    )

    password = forms.CharField(
        max_length=255, min_length=4,
        widget=forms.PasswordInput(attrs={ 'class': 'input-auth' })
    )


class SignUpForm(forms.Form):

    first_name = forms.CharField(
        max_length=40, min_length=2,
        widget=forms.TextInput(attrs={ 'class': 'input-auth' })
    )
    last_name = forms.CharField(
        max_length=40, min_length=2,
        widget=forms.TextInput(attrs={ 'class': 'input-auth' })
    )
    username = forms.CharField(
        max_length=30, min_length=4,
        widget=forms.TextInput(attrs={ 'class': 'input-auth' })
    )
    email = forms.EmailField(
        max_length=255, min_length=10,
        widget=forms.EmailInput(attrs={ 'class': 'input-auth' })
    )
    password = forms.CharField(
        max_length=255, min_length=4,
        widget=forms.PasswordInput(attrs={ 'class': 'input-auth' })
    )


class PasswordResetRequestForm(forms.Form):

    email = forms.EmailField(
        label=_('Email address'),
        max_length=200,
        min_length=4,
        widget=forms.EmailInput(attrs={ 'class': 'input-auth' })
    )


class PasswordResetForm(forms.Form):

    new_password = forms.CharField(
        max_length=256, min_length=8,
        label=_('New password'),
        widget=forms.PasswordInput(attrs={ 'class': 'input-auth' })
    )
    password_confirm = forms.CharField(
        max_length=256, min_length=8,
        label=_('Confirm new password'),
        widget=forms.PasswordInput(attrs={ 'class': 'input-auth' })
    )
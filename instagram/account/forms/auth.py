# django imports
from django import forms
from django.utils.translation import gettext_lazy as _

# Instagram forms
from instagram.core.forms import mixins


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
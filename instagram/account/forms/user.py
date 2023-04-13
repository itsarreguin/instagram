# Python standard library
from typing import Dict
from typing import List
from typing import Type

# Django imports
from django import forms
from django.db.models import Model
from django.contrib.auth import get_user_model

# Instagram models
from instagram.account.models import Profile


class EditProfileForm(forms.ModelForm):
    
    class Meta:
        model: Type[Model] = Profile
        fields: List[str] = [
            'picture',
            'link',
            'biography'
        ]
        
        widgets: Dict[str, object] = {
            'picture': forms.FileInput(attrs={}),
            'link': forms.URLInput(attrs={ 'class': 'input-settings' }),
            'biography': forms.Textarea(attrs={ 'class': 'input-settings' })
        }


class EditAccountForm(forms.ModelForm):
    
    class Meta:
        model = get_user_model()
        fields = [
            'first_name',
            'last_name',
            'username',
            'email'
        ]
        
        widgets: Dict[str, object] = {
            'first_name': forms.TextInput(attrs={ 'class': 'input-settings' }),
            'last_name': forms.TextInput(attrs={ 'class': 'input-settings' }),
            'username': forms.TextInput(attrs={ 'class': 'input-settings' }),
            'email': forms.EmailInput(attrs={ 'class': 'input-settings' }),
        }
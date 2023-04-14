# Python standard library
from typing import Dict
from typing import List
from typing import Type

# Django forms
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import ValidationError
# Django DB
from django.db.models import Model
# Django contrib package
from django.contrib.auth import get_user_model
# Django utils
from django.utils.translation import gettext_lazy as _

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


class ChangePasswordForm(PasswordChangeForm):
    
    old_password = forms.CharField(
        label=_('Old password'),
        min_length=8, max_length=256,
        widget=forms.PasswordInput(attrs={ 'class': 'input-settings' })
    )
    new_password1 = forms.CharField(
        label=_('New password'),
        min_length=8, max_length=256,
        widget=forms.PasswordInput(attrs={ 'class': 'input-settings' })
    )
    new_password2 = forms.CharField(
        label=_('Confirm new password'),
        min_length=8, max_length=256,
        widget=forms.PasswordInput(attrs={ 'class': 'input-settings' })
    )
    
    def clean_old_password(self) -> str:
        old_password = self.cleaned_data['old_password']

        if not self.user.check_password(old_password):
            raise ValidationError(_('Wrong password'))
        
        return old_password
    
    def clean_new_password2(self) -> str:
        cleaned_data = super(ChangePasswordForm, self).clean()
        new_password = cleaned_data.get('new_password1')
        password_confirm = cleaned_data.get('new_password2')

        if new_password != password_confirm:
            raise ValidationError(_('New password didn\'t match'))
        
        return cleaned_data
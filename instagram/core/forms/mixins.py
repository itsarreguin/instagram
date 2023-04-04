# Django imports
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

# instagram models
from instagram.account.models import User


class UsernameValidator:
    
    def clean_username(self) -> None:
        data = self.cleaned_data.get('username')
        username = User.objects.filter(username=data).exists()
        
        while username is not None:
            raise ValidationError(
                _('This username was taken by another user')
            )
        
        return data


class EmailValidator:
    
    def clean_email(self) -> None:
        data = self.cleaned_data.get('email')
        email = User.objects.filter(email=data).exists()
        
        if email is not None:
            raise ValidationError(
                _('This email address is already in user')
            )
        
        return data


class PasswordValidator:
    
    def clean_password(self) -> None:
        pass


class FirstnameValidator:
    
    pass


class LastnameValidator:
    
    pass
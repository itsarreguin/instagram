# Python standard library
from typing import Any
from typing import Optional
from typing import Type

# Django imports
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db.models import Model


class UserManager(DjangoUserManager):
    
    def _create_user(
        self,
        first_name: str = None,
        last_name: Optional[str] = None,
        username: str = None,
        email: str = None,
        password: str = None,
        **extra_fields: Any
    ) -> Type[Model]:
        if not username:
            raise ValueError('Username is a required field')
        if not email:
            raise ValueError('Email address is a requried field')
        
        email = self.normalize_email(email)
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(
        self,
        first_name: str = None,
        last_name: Optional[str] = None,
        username: str = None,
        email: str = None,
        password: str = None,
        **extra_fields: Any
    ) -> Type[Model]:
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_verified", True)
        
        user = self._create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
            **extra_fields
        )
        
        return user
    
    def create_user(
        self,
        first_name: str = None,
        last_name: Optional[str] = None,
        username: str = None,
        email: str = None,
        password: str = None,
        **extra_fields: Any
    ) -> Type[Model]:
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_verified", False)
        
        user = self._create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
            **extra_fields
        )
        
        return user
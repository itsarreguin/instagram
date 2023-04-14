# Python standard library
from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import Type

# Django HTTP package
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
# Django views
from django.views import View
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.contrib.auth.views import PasswordChangeView
# Django DB
from django.db.models import QuerySet
from django.db.models import Model
# Django auth and shortcuts
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render
# Django forms
from django.forms import Form
from django.forms import ModelForm
# Django urls
from django.urls import reverse
# Django utils
from django.utils.translation import gettext_lazy as _

# Instagram models
from instagram.account.models import User
from instagram.account.models import Profile
# Instagram forms
from instagram.account.forms.user import EditProfileForm
from instagram.account.forms.user import EditAccountForm
from instagram.account.forms.user import ChangePasswordForm


posts: list[dict[str, str | int]] = [
    {
        'id': 1,
        'username': 'ronacher',
        'picture': 'https://images.unsplash.com/photo-1628157588553-5eeea00af15c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=880&q=80',
        'first_name': 'Armin',
        'last_name': 'Ronacher',
        'image': 'https://images.unsplash.com/photo-1680553437316-d80361108647?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2089&q=80'
    },
    {
        'id': 2,
        'username': 'yisuscraist',
        'picture': 'https://images.theconversation.com/files/346421/original/file-20200708-3995-5ulgxa.jpg?ixlib=rb-1.1.0&q=45&auto=format&w=1000&fit=clip',
        'first_name': 'Jesus',
        'last_name': 'de Nazaret',
        'image': 'https://images.unsplash.com/photo-1672745256937-4e60a4534413?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=788&q=80'
    },
    {
        'id': 3,
        'username': 'chuck',
        'picture': 'https://images.unsplash.com/photo-1633332755192-727a05c4013d?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=880&q=80',
        'first_name': 'Chuck',
        'last_name': 'Berry',
        'image': 'https://images.unsplash.com/photo-1680585934031-8842e4cf82c3?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80'
    },
    {
        'id': 4,
        'username': 'ronacher',
        'picture': 'https://images.unsplash.com/photo-1628157588553-5eeea00af15c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=880&q=80',
        'first_name': 'Armin',
        'last_name': 'Ronacher',
        'image': 'https://images.unsplash.com/photo-1680466257600-86e0aa02cc64?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80'
    },
]


class FeedView(LoginRequiredMixin, TemplateView):
    template_name = 'users/feed.html'
    
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['posts'] = posts
        
        return context


class ProfileView(LoginRequiredMixin, DetailView):
    model: Type[Model] = get_user_model()
    template_name: str = 'users/profile.html'
    
    def get_queryset(self, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> QuerySet:
        if args or kwargs:
            return self.model.objects.filter(*args, **kwargs).first()
        
        return self.model.objects.all()
    
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user'] = self.get_queryset(username=kwargs['username'])
        
        return context
    
    def get(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
        return render(request, self.template_name)


class EditProfileView(LoginRequiredMixin, UpdateView):
    
    model: Type[Profile] = Profile
    form_class: Type[Form | ModelForm] = EditProfileForm
    template_name: str = 'users/edit_profile.html'
    template_title: str = _('Edit profile')
    
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = self.template_title
        
        return context
    
    def get_object(self, queryset: Optional[QuerySet] = ...) -> Model:
        return self.request.user.profile
    
    def get_success_url(self) -> HttpResponse:
        return reverse('account:edit-profile')


class EditAccountView(LoginRequiredMixin, UpdateView):
    
    model: Type[Model] = get_user_model()
    form_class: Type[Form | ModelForm] = EditAccountForm
    template_name: str = 'users/edit_account.html'
    template_title: str = _('Edit account')
    
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = self.template_title
        
        return context
    
    def get_object(self, queryset: Optional[QuerySet] = ...) -> Model:
        return self.request.user
    
    def get_success_url(self) -> HttpResponse:
        return reverse('account:edit-account')


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    
    form_class: Type[Form | ModelForm] = ChangePasswordForm
    template_name: str = 'users/change_password.html'
    template_title: str = _('Change password')
    
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = self.template_title

        return context
    
    def get_success_url(self) -> HttpResponse:
        return reverse('account:change-password')
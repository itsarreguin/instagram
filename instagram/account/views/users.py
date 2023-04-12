# Python standard library
from typing import Any
from typing import Dict
from typing import Tuple
from typing import Type

# Django HTTP package
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
# Django views
from django.views.generic import View
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
# Django DB
from django.db.models import QuerySet
from django.db.models import Model
# Django auth and shortcuts
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
# Django forms
from django.forms import Form
from django.forms import ModelForm
# Django utils
from django.utils.translation import gettext_lazy as _

# Instagram models
from instagram.account.models import User
# Instagram forms
from instagram.account.forms.user import EditProfileForm


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
    
    template_name: str = 'users/edit_profile.html'
    view_name: str = 'Edit profile'
    form_class: Type[Form | ModelForm] = EditProfileForm
    success_url: str = 'account:edit-profile'
    
    def get(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
        context = {
            'title': self.view_name,
            'form': self.form_class
        }
        return render(request, self.template_name, context)
    
    def put(self, request: HttpRequest, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> HttpResponse:
        return super().put(*args, **kwargs)
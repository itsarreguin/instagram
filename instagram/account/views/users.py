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
from django.views.generic.base import ContextMixin
from django.views.generic import UpdateView
from django.views.generic import TemplateView
from django.contrib.auth.views import PasswordChangeView
# Django DB
from django.db.models import QuerySet
from django.db.models import Model
# Django contrib and shortcuts
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
# Django forms
from django.forms import Form
from django.forms import ModelForm
# Django urls
from django.urls import reverse
# Django utils
from django.utils.translation import gettext_lazy as _

# Instagram models
from instagram.account.models import Profile
from instagram.posts.models import Post
# Instagram forms
from instagram.account.forms.user import EditProfileForm
from instagram.account.forms.user import EditAccountForm
from instagram.account.forms.user import ChangePasswordForm
from instagram.posts.forms import EmptyForm
from instagram.posts.forms import CommentForm


class FeedView(LoginRequiredMixin, TemplateView):
    
    template_name: str = 'users/feed.html'
    
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.order_by('-created').all()
        context['empty_form'] = EmptyForm
        context['comment_form'] = CommentForm
        
        return context


class ProfileView(LoginRequiredMixin, ContextMixin, View):
    
    model: Type[Model] = get_user_model()
    template_name: str = 'users/profile.html'
    
    def get_queryset(self, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> QuerySet:
        if args or kwargs:
            return self.model.objects.filter(*args, **kwargs).first()
        
        return self.model.objects.all()
    
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user'] = self.get_queryset(username=self.kwargs['username'])
        context['posts'] = (
            Post.objects
            .filter(author__username=self.kwargs['username'])
            .order_by('-created')
            .all()
        )
        return context
    
    def get(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)


class FollowUserView(LoginRequiredMixin, ContextMixin, View):
    
    model: Type[Model] = get_user_model()
    template_name: str = 'includes/profile-data.html'
    
    def get_queryset(self, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> QuerySet:
        return self.model.objects.filter(*args, **kwargs).first()
    
    def post(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
        user = self.get_queryset(**{ 'username': kwargs['username'] })
        if user is not None:
            user.followers.add(request.user)
            context = { 'user': user }
            return render(request, self.template_name, context)
        
        return HttpResponseRedirect(reverse('account:feed'))
    
    def delete(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
        user = self.get_queryset(**{ 'username': kwargs['username'] })
        if request.user in user.followers.all():
            user.followers.remove(request.user)
            context = { 'user': user }
            return render(request, self.template_name, context)
        
        return HttpResponseRedirect(reverse('account:feed'))


class ExploreView(LoginRequiredMixin, TemplateView):
    
    template_name: str = 'users/explore.html'
    
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all().order_by('-created')
        
        return context


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
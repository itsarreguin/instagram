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
from django.views import generic
# Django authentication
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth import logout
# Django shortcuts and urls
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
# Django forms
from django.forms import Form
from django.forms import ModelForm
# Django utils
from django.utils.translation import gettext_lazy as _

# Instagram models
from instagram.account.models import User
from instagram.account.models import Profile
# instagram forms
from instagram.account.forms.auth import LoginForm
from instagram.account.forms.auth import SignUpForm
from instagram.account.forms.auth import PasswordResetRequestForm


class LoginView(generic.View):
    template_name: str = 'auth/login.html'
    form_class: Type[Form | ModelForm] = LoginForm
    view_title: str = _('Login')
    
    def get(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
        form = self.form_class()
        
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('account:feed'))
        
        context = {
            'title': self.view_title,
            'form': form,
            'info': _('Hello from login view')
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
        form = self.form_class(request.POST)
        
        if request.method == 'POST' and form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            
            if user is not None:
                login(request, user=user)
                return HttpResponseRedirect(reverse('account:feed'))
            
            return HttpResponseRedirect(reverse('account:login'))
        
        context = {
            'title': self.view_title,
            'form': form
        }
        
        return render(request, self.template_name, context)


class SignUpView(generic.View):
    template_name: str = 'auth/signup.html'
    form_class: Type[Form | ModelForm] = SignUpForm
    view_name: str = _('Sign Up')
    
    def get(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
        form = self.form_class()
        
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('account:feed'))
        
        context = {
            'title': self.view_name,
            'form': form,
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            Profile.objects.create(user=user)
            login(request, user=user)
            
            return HttpResponseRedirect(reverse('account:feed'))
        
        context = {
            'title': self.view_name,
            'form': form,
        }
        
        return render(request, self.template_name, context)


class LogoutView(LoginRequiredMixin, generic.RedirectView):
    
    def get_redirect_url(self, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> Optional[str]:
        if self.request.user.is_authenticated:
            logout(self.request)
            return reverse('account:login')
        
        return super(LogoutView, self).get_redirect_url(*args, **kwargs)


def password_reset_request(request: HttpRequest) -> HttpResponse:
    form = PasswordResetRequestForm
    context = {
        'form': form
    }
    return render(
        request=request,
        template_name='auth/password_reset_request.html',
        context=context
    )
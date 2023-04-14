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
from django.views.generic import RedirectView
# Django authentication
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth import logout
# Django shortcuts and urls
from django.shortcuts import render
from django.urls import reverse
# Django forms
from django.forms import Form
from django.forms import ModelForm
# Django utils
from django.utils.translation import gettext_lazy as _

# Instagram models
from instagram.account.models import User
# instagram forms
from instagram.account.forms.auth import LoginForm
from instagram.account.forms.auth import SignUpForm
from instagram.account.forms.auth import PasswordResetRequestForm


class AuthContextMixin(ContextMixin):
    
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = self.template_title
        context['form'] = self.form_class
        
        return context


class LoginView(AuthContextMixin, View):
    
    form_class: Type[Form | ModelForm] = LoginForm
    template_name: str = 'auth/login.html'
    template_title: str = _('Login')
    
    def get(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('account:feed'))
        
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)
    
    def post(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
        form = self.form_class(request.POST or None)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            
            if user is not None:
                login(request, user=user)
                return HttpResponseRedirect(reverse('account:feed'))
            
            return HttpResponseRedirect(reverse('account:login'))
        
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)


class SignUpView(AuthContextMixin, View):
    
    template_name: str = 'auth/signup.html'
    form_class: Type[Form | ModelForm] = SignUpForm
    template_title: str = _('Sign Up')
    
    def get(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('account:feed'))
        
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)
    
    def post(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
        form = self.form_class(request.POST or None)
        if form.is_valid():
            user = User.objects.create_user(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            login(request, user=user)
            
            return HttpResponseRedirect(reverse('account:feed'))
        
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)


class LogoutView(LoginRequiredMixin, RedirectView):
    
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
# Python standard library
from typing import Any
from typing import Dict
from typing import Optional
from typing import Type

# Django HTTP package
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
# Django views
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
# Django authentication
from django.contrib.auth import authenticate
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

# instagram forms
from instagram.account.forms.auth import LoginForm


class LoginView(generic.View):
    template_name: str = 'auth/login.html'
    form_class: Type[Form | ModelForm] = LoginForm
    view_title: str = _('Login')
    
    def get(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
        form = self.form_class()
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
                username=request.POST['username'],
                password=request.POST['password']
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
    form_class: Type[Form | ModelForm] = None
    view_name: str
    
    def get(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
        context = {
            'title': _('Sign Up')
        }
        
        return render(request, self.template_name, context)


class LogoutView(LoginRequiredMixin, generic.RedirectView):
    
    def get_redirect_url(self, *args: Any, **kwargs: Any) -> Optional[str]:
        if self.request.user.is_authenticated:
            logout(self.request)
            return reverse('account:login')
        
        return super(LogoutView, self).get_redirect_url(*args, **kwargs)
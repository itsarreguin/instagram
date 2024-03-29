# Python standard library
from typing import Any, Dict, Optional, Type

# Django HTTP package
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
# Django views
from django.views import View
from django.views.generic.edit import FormMixin
from django.views.generic import RedirectView
# Django contrib
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.tokens import default_token_generator as token_generator
# Django shortcuts and urls
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
# Django forms
from django.forms import Form
from django.forms import ModelForm
# Django utils
from django.utils.translation import gettext_lazy as _
from django.utils.http import urlsafe_base64_decode

# Instagram models
from instagram.account.models import User
# instagram forms
from instagram.account.forms.auth import LoginForm
from instagram.account.forms.auth import SignUpForm
from instagram.account.forms.auth import PasswordResetRequestForm
from instagram.account.forms.auth import PasswordResetForm
# Instagram tasks
from instagram.account.tasks import send_user_email


class AuthContextMixin(FormMixin):

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = self.template_title
        context['form'] = self.get_form_class()

        return context


class LoginView(AuthContextMixin, View):

    form_class: Type[Form | ModelForm] = LoginForm
    template_name: str = 'auth/login.html'
    template_title: str = _('Login')

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('account:feed'))

        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
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

        return render(request, self.template_name, self.get_context_data(**kwargs))


class SignUpView(AuthContextMixin, View):

    form_class: Type[Form | ModelForm] = SignUpForm
    template_name: str = 'auth/signup.html'
    template_title: str = _('Sign Up')

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('account:feed'))

        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST or None)

        if form.is_valid():
            user = User.objects.create_user(**form.cleaned_data)
            send_user_email.apply_async(kwargs={
                'email_address': form.cleaned_data['email'],
                'subject': 'Account verification',
                'template': 'email/account_verification.html',
                'path': request.get_host()
            })
            login(request, user=user)

            return HttpResponseRedirect(reverse('account:feed'))

        return render(request, self.template_name, self.get_context_data(**kwargs))


class LogoutView(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> Optional[str]:
        if self.request.user.is_authenticated:
            logout(self.request)
            return reverse('account:login')

        return super(LogoutView, self).get_redirect_url(*args, **kwargs)


class PasswordResetRequestView(AuthContextMixin, View):

    form_class: Type[Form | ModelForm] = PasswordResetRequestForm
    template_name: str = 'auth/forgot_password.html'
    template_title: str = _('Password Reset')

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
        form = self.form_class(request.POST or None)
        if form.is_valid():
            send_user_email.apply_async(kwargs={
                'email_address': form.cleaned_data['email'],
                'subject': 'Password rest',
                'template': 'email/reset_password.html',
                'path': request.get_host()
            })
            return redirect('account:password-reset-request')

        return render(request, self.template_name, self.get_context_data(**kwargs))


class PasswordResetView(AuthContextMixin, View):

    form_class: Type[Form | ModelForm] = PasswordResetForm
    template_name: str = 'auth/password_reset.html'
    template_title: str = _('Password Reset')

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST or None)
        try:
            uid = urlsafe_base64_decode(kwargs['uidb64']).decode()
            user = get_object_or_404(User, id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        check_token = token_generator.check_token(user, kwargs['token'])
        if form.is_valid() and user is not None and check_token:
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            return redirect('account:login')

        return render(request, self.template_name, self.get_context_data(**kwargs))
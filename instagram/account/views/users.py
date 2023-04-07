# Django HTTP package
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
# Django views
from django.views.generic import DetailView
# Django auth and shortcuts
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
# Django utils
from django.utils.translation import gettext_lazy as _

# Instagram models
from instagram.account.models import User


@login_required(login_url='account:login')
def feed(request) -> HttpResponse:
    return render(request, 'users/feed.html')


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    queryset = User.objects.all()
    template_name = 'users/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'user'
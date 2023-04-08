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


@login_required(login_url='account:login')
def feed(request) -> HttpResponse:
    context = {
        'posts': posts
    }
    return render(request, 'users/feed.html', context)


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    queryset = User.objects.all()
    template_name = 'users/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'user'
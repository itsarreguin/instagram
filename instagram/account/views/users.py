# Python standard library
from typing import Any, Dict, List, Optional, Type

# Django HTTP package
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
# Django views
from django.views import View
from django.views.generic.base import ContextMixin
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.contrib.auth.views import PasswordChangeView
# Django DB
from django.db.models import QuerySet
from django.db.models import Model
from django.db.models import Prefetch
# Django contrib and shortcuts
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.shortcuts import render
from django.shortcuts import get_object_or_404
# Django forms
from django.forms import Form
from django.forms import ModelForm
# Django urls
from django.urls import reverse
# Django utils
from django.utils.translation import gettext_lazy as _
from django.utils.http import urlsafe_base64_decode

# Instagram models
from instagram.account.models import User
from instagram.account.models import Profile
from instagram.posts.models import Post
from instagram.notifications.models import NotificationType
# Instagram forms
from instagram.account.forms.user import EditProfileForm
from instagram.account.forms.user import EditAccountForm
from instagram.account.forms.user import ChangePasswordForm
from instagram.posts.forms import CommentForm
# Instagram tasks
from instagram.notifications.tasks import send_notification


class FeedView(LoginRequiredMixin, ListView):

    model: Type[Model] = Post
    template_name: str = 'users/feed.html'

    def get_queryset(self, *args: Any, **kwargs: Any) -> QuerySet[Post]:
        return Post.objects.filter(*args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['posts'] = (
            self.get_queryset(author__username=self.request.user.username)
            .union(
                self.get_queryset(author__in=self.request.user.following.all()).all()
            )
            .order_by('-created')
            .all()
        )
        context['comment_form'] = CommentForm

        return context


class ProfileView(LoginRequiredMixin, ContextMixin, View):

    model: Type[Model] = get_user_model()
    template_name: str = 'users/profile.html'

    def get_queryset(self, *args: Any, **kwargs: Any) -> QuerySet[List[Post]]:
        queryset = (
            Post.objects.order_by('-created').prefetch_related('likes', 'comments').all()
        )
        posts = Prefetch(lookup='posts', queryset=queryset)

        return self.model.objects.filter(*args, **kwargs).prefetch_related(
            'profile', 'following', 'followers', posts
        )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user'] = self.get_queryset(username=kwargs['username']).first()

        return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)


class FollowUserView(LoginRequiredMixin, View):

    model: Type[Model] = get_user_model()
    template_name: str = 'includes/profile-data.html'

    def get_queryset(self, *args: Any, **kwargs: Any) -> QuerySet[User]:
        return self.model.objects.filter(*args, **kwargs).first()

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        user = self.get_queryset(**{ 'username': kwargs['username'] })
        if user is not None:
            user.followers.add(request.user)
            send_notification.apply_async(kwargs={
                'receiver_username': user.username,
                'sender_username': request.user.username,
                'category': NotificationType.FOLLOWER,
                'object_id': request.user.pk,
                'object_slug': request.user.username
            })

            return render(request, self.template_name, { 'user': user })

        return HttpResponseRedirect(reverse('account:feed'))

    def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        user = self.get_queryset(**{ 'username': kwargs['username'] })

        if request.user in user.followers.all():
            user.followers.remove(request.user)
            return render(request, self.template_name, { 'user': user })

        return HttpResponseRedirect(reverse('account:feed'))


class ExploreView(LoginRequiredMixin, TemplateView):

    template_name: str = 'users/explore.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['posts'] = (
            Post.objects.order_by('-created').select_related('author')
                .prefetch_related('comments', 'likes').all()
        )

        return context


class AccountVerificationView(View):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        try:
            uid = urlsafe_base64_decode(kwargs['uidb64']).decode('utf-8')
            user = get_object_or_404(User, id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        verification_token = token_generator.check_token(user, kwargs['token'])
        if user is not None and verification_token:
            user.is_verified = True
            user.save()
            return HttpResponseRedirect(reverse('account:feed'))

        return HttpResponse('Account activation failed')


class EditProfileView(LoginRequiredMixin, UpdateView):

    model: Type[Profile] = Profile
    form_class: Type[Form | ModelForm] = EditProfileForm
    template_name: str = 'users/edit_profile.html'
    template_title: str = _('Edit profile')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
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

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
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

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = self.template_title

        return context

    def get_success_url(self) -> str:
        return reverse('account:change-password')
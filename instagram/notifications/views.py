# Python standard library
import json
from typing import Any, Dict, Generator, List, Type

# Django HTTP package
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.http import HttpResponseRedirect
# Django views
from django.views import generic
# Django contrib
from django.contrib.auth.mixins import LoginRequiredMixin
# Django database
from django.db.models import QuerySet
from django.db.models import Model
# Django shortcuts
from django.shortcuts import redirect
# DJango urls
from django.urls import reverse
# Django utils
from django.utils.translation import gettext_lazy as _

# Instagram models
from instagram.account.models import User
from instagram.posts.models import Post
from instagram.notifications.models import Notification
from instagram.notifications.models import NotificationType
from instagram.notifications.serializers import notification_serializer


class NotificationsView(LoginRequiredMixin, generic.ListView):

    template_name: str = 'notifications.html'
    template_title: str = _('Notifications')
    model: Type[Model] = Notification

    def get_queryset(self, *args: Any, **kwargs: Any) -> QuerySet[List[Notification]]:
        return (
            self.model.objects.filter(*args, **kwargs)
            .prefetch_related('sender', 'sender__profile')
            .order_by('-created').all()
        )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = self.template_title
        context['notifications'] = self.get_queryset(receiver=self.request.user)
        return context


class NotificationReadView(LoginRequiredMixin, generic.View):

    model: Type[Model] = Notification

    def get(self, request: HttpRequest, **kwargs: Any) -> HttpResponse:
        notification = (
            self.model.objects
            .filter(slug=kwargs['noti_slug'], object_slug=kwargs['object_slug'])
            .first()
        )
        notification.is_read = True
        notification.save()

        if notification.category == NotificationType.FOLLOWER:
            user = User.objects.get(pk=notification.object_id)
            return redirect('account:profile', username=user.username)

        elif (
            notification.category == NotificationType.LIKE or
            notification.category == NotificationType.COMMENT
        ):
            post = Post.objects.get(url=notification.object_slug)
            return redirect('posts:detail', url=post.url)

        return HttpResponseRedirect(reverse('notifications:all'))


class NotificationDeleteView(LoginRequiredMixin, generic.View):

    def get_queryset(self, *args: Any, **kwargs: Any) -> QuerySet[Notification]:
        return Notification.objects.filter(*args, **kwargs)

    def delete(self, request: HttpRequest, **kwargs: Any) -> HttpResponse:
        notification = self.get_queryset(pk=kwargs['pk'])
        if notification is not None:
            notification.delete()

        return HttpResponse()


class SSENotificationsView(LoginRequiredMixin, generic.View):

    def get_queryset(self, receiver: User) -> QuerySet[Notification]:
        return (
            Notification.objects.filter(receiver=receiver)
            .order_by('-created').all()
        )

    def notifications_generator(self) -> Type[Generator]:
        notifications = self.get_queryset(self.request.user)
        data = [
            notification_serializer(notification) for notification in notifications
        ]
        yield f'data: {json.dumps(data)}\n\n'

    def get(self, request: HttpRequest, **kwargs: Any) -> StreamingHttpResponse:
        return StreamingHttpResponse(
            self.notifications_generator(), content_type='text/event-stream'
        )
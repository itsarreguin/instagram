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
from django.views import View
from django.views.generic import TemplateView
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


class NotificationsView(LoginRequiredMixin, TemplateView):
    
    template_name: str = 'notifications.html'
    template_title: str = _('Notifications')
    
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = self.template_title
        
        return context


class NotificationReadView(LoginRequiredMixin, View):
    
    model: Type[Model] = Notification
    
    def get(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
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


class NotificationDeleteView(LoginRequiredMixin, View):
    
    def get_queryset(self, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> QuerySet:
        return Notification.objects.filter(*args, **kwargs)
    
    def delete(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
        notification = self.get_queryset(pk=kwargs['pk']).first()
        if notification:
            notification.delete()
        
        return HttpResponse()
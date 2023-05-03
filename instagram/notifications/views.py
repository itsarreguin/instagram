# Python standard library
from typing import Any
from typing import Dict
from typing import Tuple

# Django HTTP package
from django.http import HttpRequest
from django.http import HttpResponse
# Django views
from django.views import View
from django.views.generic import TemplateView
# Django contrib
from django.contrib.auth.mixins import LoginRequiredMixin
# Django database
from django.db.models import QuerySet
# Django utils
from django.utils.translation import gettext_lazy as _

# Instagram models
from instagram.notifications.models import Notification
from instagram.notifications.models import NotificationType


class NotificationsView(LoginRequiredMixin, TemplateView):
    
    template_name: str = 'notifications.html'
    template_title: str = _('Notifications')
    
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = self.template_title
        
        return context


class NotificationDeleteView(LoginRequiredMixin, View):
    
    def get_queryset(self, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> QuerySet:
        return Notification.objects.filter(*args, **kwargs)
    
    def delete(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponse:
        notification = self.get_queryset(pk=kwargs['pk']).first()
        if notification:
            notification.delete()
        
        return HttpResponse()
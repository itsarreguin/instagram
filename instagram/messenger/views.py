# Python standard library
from typing import Any, Dict, List, Type

# Django HTTP Package
from django.http import HttpRequest
from django.http import HttpResponse
# Django views
from django.views import generic
# Django contrib
from django.contrib.auth.mixins import LoginRequiredMixin
# Django DB
from django.db.models import QuerySet
# Django templates
from django.template import loader
# Django utils
from django.utils.translation import gettext_lazy as _

from instagram.core.models import BaseAbstractModel
from instagram.messenger.models import Inbox, Message
from instagram.messenger.context_processors import inboxes_context


inbox_prefetch_fields = ('users', 'users__profile')
messages_selct_fields = ('sender', 'sender__profile', 'receiver', 'receiver__profile')


class MessengerView(LoginRequiredMixin, generic.TemplateView):

    template_name: str = 'messages.html'
    template_title: str = _('Messages')

    def get_queryset(self) -> QuerySet[List[Inbox]]:
        return (
            Inbox.objects.filter(users__in=[self.request.user])
            .prefetch_related(*inbox_prefetch_fields).all()
        )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = self.template_title
        context['inboxes'] = self.get_queryset()
        return context


class InboxDetailView(LoginRequiredMixin, generic.DetailView):

    template_name: str = 'inbox.html'
    template_title: str = _('Messages')
    model: Type[BaseAbstractModel] = Inbox

    def get_queryset(self, *args: Any, **kwargs: Any) -> QuerySet[Inbox]:
        return self.model.objects.filter(*args, **kwargs).first()

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        inbox = self.get_queryset(uuid=kwargs['uuid'])
        messages = (
            Message.objects.filter(inbox=inbox).select_related(*messages_selct_fields).all()
        )

        template = loader.get_template('inbox.html')
        context = {
            'title': self.template_title,
            'inbox': inbox,
            'messages': messages,
            **inboxes_context(request)
        }
        return HttpResponse(template.render(context, request))
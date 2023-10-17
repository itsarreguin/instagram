# Python standard library
from typing import Any
from typing import Dict

# Django HTTP package
from django.http import HttpRequest
from django.http import HttpResponse
# Django views
from django.views import generic
# Django contrib
from django.contrib.auth.mixins import LoginRequiredMixin
# Django shortcuts
from django.shortcuts import render
# Django utils
from django.utils.translation import gettext_lazy as _


class MessengerView(LoginRequiredMixin, generic.TemplateView):

    template_name: str = 'inbox.html'
    template_title: str = _('Messages')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = self.template_title
        return context
# Python standard library
from typing import Any
from typing import Dict

# Django views
from django.views.generic import TemplateView
# Django contrib
from django.contrib.auth.mixins import LoginRequiredMixin
# Django utils
from django.utils.translation import gettext_lazy as _


class NotificationsView(LoginRequiredMixin, TemplateView):
    
    template_name: str = 'notifications.html'
    template_title: str = _('Notifications')
    
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = self.template_title
        
        return context
from typing import Any

from django.http import HttpRequest

from instagram.messenger.models import Inbox


def inboxes_context(request: HttpRequest) -> dict[str, Any]:
    if request.user.is_authenticated:
        return {
            'inboxes': (
                Inbox.objects.filter(users__in=[request.user])
                .prefetch_related('users', 'users__profile').all()
            )
        }
    return {}
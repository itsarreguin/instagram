# Django imports
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.translation import gettext_lazy as _

# Instagram celery
from instagram import celery
# Instagram models
from instagram.account.models import User
# Instagram utils
from instagram.core.utils.email import send_email_multi_alternatives


@celery.task(max_retries=6)
def send_password_reset_email(email_address: str, path: str):
    try:
        user = get_object_or_404(User, email=email_address)
    except get_user_model().DoesNotExist:
        user = None
    
    send_email_multi_alternatives(
        subject=_('Password reset'),
        template_name='email/reset_password.html',
        from_email=settings.DEFAULT_FROM_EMAIL,
        receiver=[user.email],
        context={
            'user': user,
            'path': path,
            'uid': urlsafe_base64_encode(force_bytes(user.id)),
            'token': default_token_generator.make_token(user)
        }
    )
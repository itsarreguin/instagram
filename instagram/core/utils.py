""" Utils from the core """

# Django imports
from django.http import HttpRequest
from django.contrib.sites.shortcuts import get_current_site
from django.template import loader
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

# instagram models
from instagram.account.models import User


UPPER_CHARS = 'ABCDEFGHIJKLMNOPKRSTUVWXYZ'

LOWER_CHARS = 'abcdefghijklmnopkrstuvwxyz'

NUMBER_CHARS = '123456789'

SPECIAL_CHARS = '-_'

RAND_CHARS = UPPER_CHARS + LOWER_CHARS + NUMBER_CHARS + SPECIAL_CHARS


def gen_user_token(request: HttpRequest, user: User, template: str):
    context = {
        'user': user,
        'domain': get_current_site(request),
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': default_token_generator.make_token(user)
    }
    message = loader.render_to_string(template, context)
    print(message)
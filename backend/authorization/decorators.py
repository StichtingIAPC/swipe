import collections
import datetime

from django.core.exceptions import PermissionDenied
from django.utils import timezone
from rest_framework.authtoken.models import Token

from swipe import settings


def authenticate(username=False, token=False, perms=None):
    def _auth_decorator(view):
        def _wrapper_func(request, *args, **kwargs):
            user = _post_auth(request.POST, username_auth=username, token_auth=token)

            if user is None:
                raise PermissionDenied

            if perms is None or (
            user.has_perms(perms) if isinstance(perms, collections.Sequence) else user.has_perm(perms)):
                return view(request, *args, **kwargs)

        return _wrapper_func

    return _auth_decorator


def _post_auth(POST, username_auth=False, token_auth=False):
    if not token_auth and not username_auth:
        return None

    tokens = Token.objects
    if username_auth:
        tokens = tokens.filter(user__username=POST['username'])

    if token_auth:
        tokens = tokens.filter(key=POST['token'])

    if tokens.count() == 1 and tokens.first().created + datetime.timedelta(
            hours=settings.AUTH_TOKEN_VALID_TIME_HOURS) > timezone.now():
        return tokens.first().user


def _session_auth(session):
    return Token.objects.filter(key=session['auth.token']).first().user


def _cookie_auth():
    pass

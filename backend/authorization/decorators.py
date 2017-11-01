import datetime

from django.core.exceptions import PermissionDenied
from django.utils import timezone
from rest_framework.authtoken.models import Token

from swipe import settings


def authenticate(username=False, token=False, perm=None):
    def _auth_wrapper_func(view):
        def _wrapper_func(request, *args, **kwargs):
            if not token and not username:
                raise PermissionDenied

            tokens = Token.objects
            if username:
                tokens = tokens.filter(user__username=request.POST['username'])

            if token:
                tokens = tokens.filter(key=request.POST['token'])

            if tokens.count() == 1 and tokens.first().created + datetime.timedelta(
                    hours=settings.AUTH_TOKEN_VALID_TIME_HOURS) > timezone.now():
                if perm is None or tokens.first().user.has_perm(perm):
                    return view(request, *args, **kwargs)
            raise PermissionDenied

        return _wrapper_func

    return _auth_wrapper_func

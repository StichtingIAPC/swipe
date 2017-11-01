import datetime

from django.core.exceptions import PermissionDenied
from django.utils import timezone
from rest_framework.authtoken.models import Token

from swipe import settings


def authenticate(mode, perm):
    def _auth_wrapper_func(view):
        def _wrapper_func(request, *args, **kwargs):
            if mode == 'username,token' or mode == 'token,username':
                tokens = Token.objects.filter(key=request.POST['token']).filter(user__username=request.POST['username'])
            elif mode == 'username':
                tokens = Token.objects.filter(user__username=request.POST['username'])
            elif mode == 'token':
                tokens = Token.objects.filter(key=request.POST['token'])
            else:
                raise PermissionDenied

            if tokens.count() == 1 and tokens.first().created + datetime.timedelta(
                    hours=settings.AUTH_TOKEN_VALID_TIME_HOURS) > timezone.now():
                if perm is None or tokens.first().user.has_perm(perm):
                    return view(request, *args, **kwargs)
            raise PermissionDenied

        return _wrapper_func

    return _auth_wrapper_func

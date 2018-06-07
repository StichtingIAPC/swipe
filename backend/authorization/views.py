import hashlib
from datetime import timedelta
from django.conf import settings
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import serializers

User = settings.AUTH_USER_MODEL


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super().__init__(content, **kwargs)


class Logout(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(Logout, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        if 'token' not in request.POST or request.POST['token'] is None:
            return JSONResponse({})
        Token.objects.filter(key=request.POST['token']).delete()
        return JSONResponse({})


class Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError:
            return HttpResponse(status=401, content="Username or password incorrect")
        user = serializer.validated_data['user']
        Token.objects.filter(user=user).filter(
            created__lt=timezone.now() - timedelta(hours=settings.AUTH_TOKEN_VALID_TIME_HOURS)).delete()
        token, created = Token.objects.get_or_create(user=user)

        m = hashlib.md5()
        m.update(user.email.encode('utf-8'))

        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'permissions': user.get_all_permissions(),
                'gravatarUrl': 'https://www.gravatar.com/avatar/' + m.hexdigest(),
                'firstName': user.first_name,
                'lastName': user.last_name,
                'email': user.email,
            },
        })


class Validate(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(Validate, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        tokens = Token.objects.filter(key=request.POST['token']).filter(user__username=request.POST['username'])

        if tokens.count() == 1:
            token = tokens.first()
            user = token.user

            expiry = (timezone.now() if token.created is None else token.created) + timedelta(
                hours=settings.AUTH_TOKEN_VALID_TIME_HOURS)

            if expiry < timezone.now():
                return JSONResponse({
                    'valid': False,
                    'expiry': expiry.strftime('%Y-%m-%d %H:%M'),
                })

            m = hashlib.md5()
            m.update(user.email.encode('utf-8'))

            return JSONResponse({
                'valid': True,
                'expiry': expiry.strftime('%Y-%m-%d %H:%M'),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'permissions': user.get_all_permissions(),
                    'gravatarUrl': 'https://www.gravatar.com/avatar/' + m.hexdigest(),
                    'firstName': user.first_name,
                    'lastName': user.last_name,
                    'email': user.email,
                }
            })

        return JSONResponse({
            'valid': False,
        })

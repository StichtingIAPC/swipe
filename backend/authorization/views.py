from django.conf import settings
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

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
        Token.objects.filter(key=request.POST['token']).delete()
        return JSONResponse({})


class Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': {
                'username': user.username,
                'permissions': user.get_all_permissions(),
                'gravatarUrl': 'https://www.gravatar.com/avatar/00000000000000000000000000000000',
            },
        })


class UserProfile(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(UserProfile, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        tok = Token.objects.filter(key=request.POST['token']).all()
        if len(tok) <= 0:
            return JSONResponse({
                'error': 'No user found',
                'token': request.POST['token'],
            })

        user = tok.get().user
        return JSONResponse({
            'user': {
                'username': user.username,
                'firstName': user.first_name,
                'lastName': user.last_name,
                'email': user.email,
                'gravatarUrl': 'https://www.gravatar.com/avatar/00000000000000000000000000000000',
            },
        })

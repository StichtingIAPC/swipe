from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer



User = settings.AUTH_USER_MODEL


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super().__init__(content, **kwargs)


@csrf_exempt
def logout(request):
    if request.method == 'POST':
        Token.objects.filter(key=request.POST['token']).delete()
        return JSONResponse({})


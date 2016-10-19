import json

from django.http import HttpRequest

from swipe import settings


def swipe_globals(request):
    """
    :param request:
    :type request: HttpRequest
    :return:
    """
    context = {
        'SWIPE_JS_GLOBAL_VARS': json.dumps(settings.SWIPE_JS_GLOBAL_VARS),
        'current_view': resolve(request.resolver_match.view_name)
    }

    return context

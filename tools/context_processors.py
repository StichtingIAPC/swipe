import json

from swipe import settings


def swipe_globals(request):
    context = {
        'SWIPE_JS_GLOBAL_VARS': json.dumps(settings.SWIPE_JS_GLOBAL_VARS)
    }

    return context

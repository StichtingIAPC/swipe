from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated

import swipe.settings


class SwipeLoginRequired:
    """
    The view that is inheriting from this should also directly or indirectly inherit from rest_framework.views.APIView
    """
    permission_classes = () if hasattr(swipe.settings, "SECURITY_DISABLED") and swipe.settings.SECURITY_DISABLED else\
        (IsAuthenticated,)

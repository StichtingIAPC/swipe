import inspect

from django.apps import AppConfig
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from rest_framework.exceptions import PermissionDenied
from crm.models import SwipePermission

import swipe.settings


class SwipeLoginRequired(LoginRequiredMixin):
    """
    The Swipe implementation of checking if the user who tried to access an endpoint was logged in. Any view that
    should be protected by user authentication should inherit from this class FIRSTLY. If done later in the inheritance
    chain it might be skipped.
    """

    def __init__(self):
        super(SwipeLoginRequired, self).__init__()
        self.raise_exception = True

    def handle_no_permission(self):
        if self.raise_exception:
            return HttpResponse('401 Unauthorized', status=401)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            if hasattr(swipe.settings, "SECURITY_DISABLED"):
                security = swipe.settings.SECURITY_DISABLED
            else:
                security = None
            if security is None or security is not True:
                return self.handle_no_permission()
        # The super 'dispatch' call does not exist for this Mixin
        # Other mixins provide this functionality
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


def swipe_authorize(request, permission):
    """
    :param request: the request object from the View
    :type request: rest_framework.request.Request
    :param permission: a string with the specified permission
    :type permission: str
    :return:
    """
    security = None
    if hasattr(swipe.settings, "SECURITY_DISABLED"):
        security = swipe.settings.SECURITY_DISABLED
    if security:
        return
    if not request.user.is_authenticated or (not request.user.is_superuser
                                             and not SwipePermission.user_has_permission(request.user, permission)):
        raise PermissionDenied
    return

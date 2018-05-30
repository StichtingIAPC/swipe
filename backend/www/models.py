from django.core.exceptions import PermissionDenied
from crm.models import SwipePermission
from rest_framework.permissions import IsAuthenticated
import swipe.settings


class SwipeLoginRequired:
    """
    The view that is inheriting from this should also directly or indirectly inherit from rest_framework.views.APIView
    """
    permission_classes = () if hasattr(swipe.settings, "SECURITY_DISABLED") and swipe.settings.SECURITY_DISABLED else\
        (IsAuthenticated,)


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


def swipe_auth(permission):
    """
    Decorator for the endpoints. Should contain the string version of the persmission
    :type permission: str
    :param permission: The permission string of the permission to check
    :return: Does a permission check and returns a PermissionDenied if not the case
    """
    def swipe_auth_decorator(func):
        def func_wrapper(zelf, request, *args, **kwargs):
            swipe_authorize(request, permission)
            return func(zelf, request, *args, **kwargs)
        return func_wrapper
    return swipe_auth_decorator

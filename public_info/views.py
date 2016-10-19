from django.http import Http404
from django.shortcuts import get_object_or_404

# Create your views here.
from django.views import View

from public_info import models


PUBLIC_VIEWS = {}


def public_view_router_view(request, random_str, *args, **kwargs):
    """
    :param request:
    :param random_str: The random string of items that makes
    :param args:
    :param kwargs:
    :return:
    """
    obj = get_object_or_404(models.Sharing, random_str=random_str)
    try:
        view = PUBLIC_VIEWS[obj.sharing_type.model_class()]
        return view(request, id=obj.sharing_id, *args, **kwargs)
    except KeyError:
        raise Http404(_("Object does not exist"))


def public_view(cls_type=None):
    """
    Decorator to say 'this class rou
    :param cls_type:
    :return:
    """
    def decorate(view):
        if issubclass(view, View):
            view = view.as_view()
        PUBLIC_VIEWS[cls_type] = view
        return view
    return decorate


def get_public_view(cls_type):
    if PUBLIC_VIEWS[cls_type]:
        return PUBLIC_VIEWS[cls_type]
    raise SharedViewNotFoundException


class SharedViewNotFoundException(Exception):
    pass

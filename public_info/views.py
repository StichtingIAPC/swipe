from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from public_info.models import Sharing, PUBLIC_VIEWS


def public_view_router_view(request, random_str, *args, **kwargs):
    """
    :param request:
    :param random_str: The random string of items that makes
    :param args:
    :param kwargs:
    :return:
    """
    obj = get_object_or_404(Sharing, random_str=random_str)
    try:
        view = PUBLIC_VIEWS[obj.sharing_type.model_class()]
        return view(request, id=obj.sharing_id, *args, **kwargs)
    except KeyError:
        raise Http404(_("Object does not exist"))

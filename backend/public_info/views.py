import uuid

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from public_info.models import Sharing


def public_view_router_view(request, uuid_str, *args, **kwargs):
    """
    :param request:
    :param uuid_str: the string form of UUID
    :param args:
    :param kwargs:
    :return:
    """
    obj = get_object_or_404(Sharing, uuid=uuid.UUID(hex=uuid_str))
    try:
        return obj.sharing_object.get_shared_view()(request, id=obj.sharing_id, *args, **kwargs)
    except KeyError:
        raise Http404(_("Object does not exist"))

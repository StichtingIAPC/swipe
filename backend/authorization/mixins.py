from django.utils.decorators import method_decorator

from authorization.decorators import authenticate


def CheckPermissionMixin(mode, perm=None):
    class CPM(object):
        @method_decorator(authenticate(mode, perm))
        def dispatch(self, request, *args, **kwargs):
            return super(CPM, self).dispatch(request, *args, **kwargs)

    return CPM

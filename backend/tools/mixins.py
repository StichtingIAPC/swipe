from django.utils.decorators import method_decorator


def MethodDecoratorMixin(decorator):
    class MDM(object):
        @method_decorator(decorator)
        def dispatch(self, request, *args, **kwargs):
            return super(MDM, self).dispatch(request, *args, **kwargs)

    return MDM

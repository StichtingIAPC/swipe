from collections import defaultdict

from django import template
from django.template import Context
from django.urls import reverse, resolve, Resolver404


register = template.Library()


KNOWN_CRUMBS = defaultdict(lambda: None)


@register.inclusion_tag("tools/partials/breadcrumbs.html", name='breadcrumbs', takes_context=True)
def breadcrumbs(context):
    """
    :param context:
    :type context: Context
    :return:
    """
    request = context['request']
    if request is None:
        raise template.TemplateSyntaxError(
            'Context does not have a "request" field: Is this tag not used in a top-level template, or in a '
            'restricted context?'
        )

    func, args, kwargs = request.resolver_match

    if hasattr(func, 'view_class'):
        view = func.view_class
    else:
        view = func

    crumbs = []
    reverse_result = ''

    while KNOWN_CRUMBS[view] is not None:
        text, parent, parent_kwargs = KNOWN_CRUMBS[view]

        crumbs.append({
            'text': text,
            'url': reverse_result
        })

        kwargs = {key: kwargs[key] for key in parent_kwargs}
        reverse_result = reverse(parent, kwargs=kwargs) if parent is not None else None

        try:
            view, a, kw = resolve(reverse_result)
            if hasattr(view, 'view_class'):
                view = view.view_class
        except Resolver404:
            view = None  # this is normal when None is being resolved

    crumbs.reverse()
    return {
        'crumbs': crumbs
    }


def crumb(name, parent=None, parent_kwargs=[]):
    if KNOWN_CRUMBS[parent] is not None:
        text, p, p_kw = KNOWN_CRUMBS[parent]
        if p is not None:
            for key in p_kw:
                if key not in parent_kwargs:
                    raise IncorrectCrumbException("Your crumb misses keyword {} for it's parent view".format(key))

    def decorator(view):
        KNOWN_CRUMBS[view] = (name, parent, parent_kwargs)
        return view
    return decorator


class IncorrectCrumbException(Exception):
    pass

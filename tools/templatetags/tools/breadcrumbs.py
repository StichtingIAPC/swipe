from django import template
from django.template import Context



register = template.Library()


CURRENT_CRUMBS = {}


@register.inclusion_tag(name='breadcrumbs', takes_context=True)
def breadcrumbs(context):
    """
    :param context:
    :type context: Context
    :return:
    """


class BreadCrumbRenderer(template.Node):
    template = Template

    def __init__(self, tags):
        pass

    def render(self, context):
        return template


def crumb(parent):
    def decorator(view):
        CURRENT_CRUMBS[view] = parent
    return decorator

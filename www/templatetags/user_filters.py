from django import template
from django.template.defaultfilters import stringfilter

from register.models import RegisterMaster

register = template.Library()


@register.filter
def display_name(user):
    """Returns the user's full name if it is set, or the username if not."""
    if hasattr(user, 'person'):
        name = user.person.name
    else:
        name = user.username

    return name


@register.filter(is_safe=True)
@stringfilter
def posessive(string):
    if len(string) > 0 and string[-1] == 's':
        return "'"
    else:
        return "'s"

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


@register.filter()
def can(user, perm):
    """
    Check if a user has a given permission
    :param user: The user to check
    :type user: User
    :param perm: The permission to check for
    :type perm: str
    :return: True if the user has the permission, False if not
    :rtype: bool
    """
    return user.has_perm(perm)


@register.filter(is_safe=True)
@stringfilter
def posessive(string):
    if len(string) > 0 and string[-1] == 's':
        return "'"
    else:
        return "'s"

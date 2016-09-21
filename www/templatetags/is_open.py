from django import template

from register.models import RegisterMaster

register = template.Library()


@register.simple_tag
def is_register_open():
    """Returns a boolean if the Swipe register is open."""
    return RegisterMaster.sales_period_is_open()

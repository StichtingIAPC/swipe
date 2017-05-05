import datetime
from django import template

register = template.Library()


@register.filter
def invoicenr(obj):
    cur_board = 28
    date = datetime.datetime.now()
    cur_year = date.strftime("%y")
    cur_month = date.strftime("%m")
    nr = obj['receipt_id']
    return "{}.{}{}.{}".format(cur_board, cur_year, cur_month, nr)

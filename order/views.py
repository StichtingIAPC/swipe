from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from money.columns import MoneyColumn
from order.models import Order, OrderCombinationLine, OrderLineState
from tools.tables import Table, Column
from public_info.views import public_view


class OrderView(TemplateView):
    template_name = 'order/view_order.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        order_id = kwargs['order_id']


@public_view(Order)
class PublicOrderView(TemplateView):
    template_name = 'order/view_public_order.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        order_id = kwargs['order_id']
        order = Order.objects.select_related('customer').get(pk=order_id)
        order_lines = list(OrderCombinationLine.get_ol_combinations(
            order=order,
        ))

        order_table = Table(
            columns=[
                Column(
                    key=lambda line: line.wishable.name,
                    name=_('Article name')
                ),
                Column(
                    key=lambda line: line.number,
                    name=_('Number')
                ),
                MoneyColumn(
                    key=lambda line: line.price,
                    name=_('Price per')
                ),
                MoneyColumn(
                    key=lambda line: line.price * line.number,
                    name=_('Price subtotal')
                )
            ],
            dataprovider=order_lines,
            classes=[]
        )

        ctx['order'] = order
        ctx['order_table'] = order_table
        return ctx

from django.conf import settings

from order.models import OrderLine, OrderCombinationLine
from tools.messaging.mail import SwipeMail


class OrderArrivedMail(SwipeMail):
    string_template = 'order/mail/order_arrived.txt'
    reply_to = settings.SWIPE_POS_MAIL

    def __init__(self, orders):
        self.customer = orders[0].customer
        for order in orders:
            if order.customer != self.customer:
                raise MailSentToIncorrectPersonException

        arrived_products = OrderLine.objects.filter(order__in=orders, state='A')
        arrived_products_combined = OrderCombinationLine.get_ol_combinations(qs=arrived_products)
        self.arrived_products = list(arrived_products_combined)

        unarrived_products = OrderLine.objects.filter(order__in=orders, state__in=['O', 'L'])
        unarrived_products_combined = OrderCombinationLine.get_ol_combinations(qs=unarrived_products)
        self.unarrived_products = list(unarrived_products_combined)

        super().__init__(to_customers=[self.customer])

    def get_context(self):
        ctx = super().get_context()
        ctx.update({
            'customer': self.customer,
            'arrived_products': self.arrived_products,
            'unarrived_products': self.unarrived_products
        })


class MailSentToIncorrectPersonException(Exception):
    """
    raised when a mail is sent to someone who should not get that mail, e.g. the status of an order is
    sent to another customer
    """
    pass

from stock.models import StockChange
from stock.stocklabel import OrderLabel
from django.db.models.signals import post_save
from django.dispatch import receiver
from order.models import OrderLine, InconsistencyError


@receiver(post_save, sender=StockChange)
def stock_change_handler(sender, **kwargs):
    stock_change = kwargs['instance']  # type: StockChange
    if stock_change.change_set.enum == 0:
        if stock_change.labeltype == "Order":
            if not stock_change.is_in:
                # This means something was sold!
                orders_to_complete = stock_change.count
                order_number = stock_change.labelkey
                art_type = stock_change.article
                lines = OrderLine.objects.filter(order_id=order_number, state='A',
                                                 wishable__sellabletype__articletype=art_type)
                if len(lines) < orders_to_complete:
                    raise InconsistencyError("Something happened and there are not enough OrderLines to transition"
                                             "to 'sold' for order {}. I cannot fix this :( Have fun fixing it in the"
                                             "database".format(order_number))
                else:
                    for i in range(orders_to_complete):
                        # We do need a hack for the user. But things work for the rest.
                        lines[i].sell(lines[i].user_modified)

    # Nothing else (yet!)
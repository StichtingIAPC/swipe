from django.db.models.signals import post_save
from django.dispatch import receiver

from stock.models import StockChange, StockChangeSet
from stock.stocklabel import OrderLabel
from order.models import OrderLine, InconsistencyError


# noinspection PyUnusedLocal
@receiver(post_save, sender=StockChange)
def stock_change_handler(sender, **kwargs):
    stock_change = kwargs['instance']  # type: StockChange
    remove_orderlines(stock_change)


def remove_orderlines(stock_change: StockChange):
    """
    Removes orderLines from state arrived to whichever state relevant.
    :param stock_change: The StockChange to be checked for orderLines
    :return:
    """
    acted_upon = [StockChangeSet.SOURCE_CASHREGISTER, StockChangeSet.SOURCE_INTERNALISE, StockChangeSet.SOURCE_STOCKCOUNT]
    source_val = stock_change.change_set.source
    if stock_change.labeltype == OrderLabel.labeltype and source_val in acted_upon:
        if not stock_change.is_in:
            orders_to_complete = stock_change.count
            order_number = stock_change.labelkey
            art_type = stock_change.article
            lines = list(OrderLine.objects.filter(order_id=order_number, state='A',
                                                  wishable__sellabletype__articletype=art_type))
            if len(lines) < orders_to_complete:
                action = ""
                if source_val == StockChangeSet.SOURCE_CASHREGISTER:
                    action = "Something happened and there are not enough OrderLines to transition " \
                             "to 'sold' for order {}. I cannot fix this :( Have fun fixing it in the" \
                             "database"
                elif source_val == StockChangeSet.SOURCE_INTERNALISE:
                    action = "Something happened and there are not enough OrderLines to transition " \
                             "to 'internalised' for order {}. I cannot fix this :( Have fun fixing it in the" \
                             "database"
                elif source_val == StockChangeSet.SOURCE_STOCKCOUNT:
                    action = "Something happened and there are not enough OrderLines to transition " \
                             "to 'cancelled' for order {}. I cannot fix this :( Have fun fixing it in the" \
                             "database"
                raise InconsistencyError(action.format(order_number))
            else:
                for i in range(orders_to_complete):
                    # We do need a hack for the user. But things work for the rest.
                    if source_val == StockChangeSet.SOURCE_CASHREGISTER:
                        lines[i].sell(lines[i].user_modified)
                    elif source_val == StockChangeSet.SOURCE_INTERNALISE:
                        lines[i].use_for_internal_purposes(lines[i].user_modified)
                    elif source_val == StockChangeSet.SOURCE_STOCKCOUNT:
                        lines[i].cancel(lines[i].user_created)

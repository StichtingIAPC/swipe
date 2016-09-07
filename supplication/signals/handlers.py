from stock.models import StockChange
from stock.stocklabel import OrderLabel

__author__ = 'lkaap'

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=StockChange)
def stock_change_handler(sender, **kwargs):
    if sender.labeltype != OrderLabel.labeltype:
        return
    if sender.is_in: # In line
        pass
    else: # Product got lost
        pass

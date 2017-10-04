from django.db.models.signals import post_save
from django.dispatch import receiver

from stock.models import StockChange


"""
Example usage of a signal:

@receiver(post_save, sender=StockChange)
def example_handler(sender, **kwargs):
    print(sender)

"""

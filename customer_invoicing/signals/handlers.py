from django.db.models.signals import post_save
from django.dispatch import receiver
from sales.models import Transaction, Payment
from register.models import PaymentType


@receiver(post_save, sender=Transaction)
def stock_change_handler(sender, **kwargs):
    # Doesn't work due to multiple item saving. Remind me to do it in function.
    transaction = kwargs['instance']  # type: Transaction
    payment_types_of_transaction = PaymentType.objects.filter(payment__transaction=transaction)
    print(payment_types_of_transaction)
    if len(payment_types_of_transaction) > 0:
        payments = Payment.objects.filter(transaction=transaction).select_related("payment_type")
        print("Yolo!")



from django.db import models, transaction
from crm.models import Customer
from blame.models import Blame, ImmutableBlame
from money.models import MoneyField
from sales.models import Transaction, RefundTransactionLine, TransactionLine, SalesTransactionLine


class RMACause(Blame):
    pass


class StockRMA(RMACause):

    value = MoneyField()


class CustomerRMATask(models.Model):

    customer = models.ForeignKey(Customer)

    description = models.TextField()

    state = models.CharField(max_length=3)

    receipt = models.ForeignKey(Transaction)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.state not in CustomerRMATaskState.STATES:
            raise StateError("While saving CustomerRMATask encountered illegal state {}".format(self.state))
        super(CustomerRMATask, self).save()


class TestRMA(RMACause):

    customer_rma_task = models.ForeignKey(CustomerRMATask)

    transaction_line = models.ForeignKey(TransactionLine)

    def save(self, **kwargs):
        if isinstance(self.transaction_line, SalesTransactionLine):
            # You cannot
            count = 0
            internal_rmas = InternalRMA.objects.filter(rma_cause__transaction_line=self.transaction_line)
            for in_rma in internal_rmas:
                if in_rma.state in InternalRMAState.OPEN_STATES:
                    count += 1
            if count >= self.transaction_line.count:
                raise RMACountError("You tried to open more active RMAs than there are counts for transaction {}".
                                    format(self.transaction_line))

        # Everything checks out, lets save
        # Consider that we must make an internal RMA for a physical product
        with transaction.atomic():
            if isinstance(self.transaction_line, SalesTransactionLine):
                internal_rma = InternalRMA(rma_cause=self, state='B')
                internal_rma.save()
            super(TestRMA, self).save()


class DirectRefundRMA(RMACause):

    refund_line = models.ForeignKey(RefundTransactionLine)


class CustomerRMATaskState(ImmutableBlame):
    STATES = ('U', 'N', 'W', 'R', 'F', 'A', 'O')
    STATE_MEANINGS = {'U': 'Untested', 'N': 'Not broken', 'W': 'Waiting for handling', 'R': 'Returned new product',
                      'F': 'Refunded', 'A': 'Customer Abuse', 'O': 'Returned original product(s) to customer'}
    OPEN_STATES = ('U', 'N', 'W', 'A')
    CLOSED_STATES = ('R', 'F', 'O')

    customer_rma_task = models.ForeignKey(CustomerRMATask)


class InternalRMA(Blame):

    rma_cause = models.ForeignKey(RMACause)

    state = models.CharField(max_length=3)

    def save(self, **kwargs):
        if self.state not in InternalRMAState.STATES:
            raise StateError("While saving InternalRMA encountered illegal state {}".format(self.state))


class InternalRMAState(ImmutableBlame):
    STATES = ('B', 'W', 'R', 'S', 'P', 'A', 'F', 'O')
    STATE_MEANINGS = {'B': 'Broken', 'W': 'Waiting for Number', 'R': 'Received number', 'S': 'Sent',
                      'P': 'Received replacement or refurbishment',
                      'A': 'Customer Abuse', 'F': 'Refunded', 'T': 'Returned product to customer', 'O': 'Written Off'}
    OPEN_STATES = ('B', 'W', 'R', 'S', 'P', 'A')
    CLOSED_STATES = ('F', 'T', 'O')

    internal_rma = models.ForeignKey(InternalRMA)


class StateError(Exception):
    pass


class RMACountError(Exception):
    pass


class MatchingException(Exception):
    pass


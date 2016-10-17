from django.db import models, transaction
from crm.models import Customer
from blame.models import Blame, ImmutableBlame
from money.models import MoneyField
from sales.models import Transaction, RefundTransactionLine, TransactionLine, SalesTransactionLine
from article.models import ArticleType


class RMACause(Blame):
    """
    The reason why an RMA has entered the system for us. The type effects how it is handled in the system.
    """
    pass


class StockRMA(RMACause):
    """
    A broken product in the stock. Just for stock and not for a customer.
    """
    article_type = models.ForeignKey(ArticleType)

    value = MoneyField()


class CustomerRMATask(models.Model):
    """
    A task where a customer has a problem with products he bought. This can be result in a number of products that are
    broken and need to be handled. Connects to a receipt.
    """
    # The customer
    customer = models.ForeignKey(Customer)

    handled = models.BooleanField(default=False)

    receipt = models.ForeignKey(Transaction)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.state not in CustomerRMATaskState.STATES:
            raise StateError("While saving CustomerRMATask encountered illegal state {}".format(self.state))
        super(CustomerRMATask, self).save()


class CustomerTaskDescription(Blame):
    """
    A description of the situation of the customer-RMA. Intended as a human readable/writable log.
    """

    customer_rma_task = models.ForeignKey(CustomerRMATask)

    text = models.TextField()


class TestRMA(RMACause):
    """
    An issue for an individual product,
    """

    customer_rma_task = models.ForeignKey(CustomerRMATask)

    transaction_line = models.ForeignKey(TransactionLine)

    state = models.CharField(max_length=3)

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
    """
    A cause for an RMA that happens when a customer is instantly refunded when he returns a (broken) product.
    """

    refund_line = models.ForeignKey(RefundTransactionLine)


class CustomerRMATaskState(ImmutableBlame):
    """
    The state log for the handling of an RMA for the customer.
    """
    STATES = ('U', 'N', 'W', 'R', 'F', 'A', 'O')
    STATE_MEANINGS = {'U': 'Untested', 'N': 'Not broken', 'W': 'Waiting for handling', 'R': 'Returned new product',
                      'F': 'Refunded', 'A': 'Customer Abuse', 'O': 'Returned original product(s) to customer'}
    OPEN_STATES = ('U', 'N', 'W', 'A')
    CLOSED_STATES = ('R', 'F', 'O')

    customer_rma_task = models.ForeignKey(CustomerRMATask)

    state = models.CharField(max_length=3)


class InternalRMA(Blame):
    """
    The handling of a broken product on 'our' side. This tracks whether we are credited for a product or it is replaced.
    Not neccesarily a concern for the customer although this means in practice that the customer has to wait for our
    handling of the problem.
    """

    rma_cause = models.ForeignKey(RMACause)

    state = models.CharField(max_length=3)

    def save(self, **kwargs):
        if self.state not in InternalRMAState.STATES:
            raise StateError("While saving InternalRMA encountered illegal state {}".format(self.state))


class InternalRMAState(ImmutableBlame):
    """
    A logger for all internal RMAs
    """
    STATES = ('B', 'W', 'R', 'S', 'P', 'A', 'F', 'O')
    STATE_MEANINGS = {'B': 'Broken', 'W': 'Waiting for Number', 'R': 'Received number', 'S': 'Sent',
                      'P': 'Received replacement or refurbishment',
                      'A': 'Customer Abuse', 'F': 'Refunded', 'T': 'Returned product to customer', 'O': 'Written Off'}
    OPEN_STATES = ('B', 'W', 'R', 'S', 'P', 'A')
    CLOSED_STATES = ('F', 'T', 'O')

    internal_rma = models.ForeignKey(InternalRMA)

    state = models.CharField(max_length=3)


class StateError(Exception):
    pass


class RMACountError(Exception):
    pass


class MatchingException(Exception):
    pass


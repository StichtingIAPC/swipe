from django.db import models, transaction
from crm.models import Customer
from blame.models import Blame, ImmutableBlame
from money.models import MoneyField
from sales.models import Transaction, RefundTransactionLine, TransactionLine, SalesTransactionLine
from article.models import ArticleType
from stock.models import Stock, StockChangeSet
from stock.enumeration import enum


class RMACause(Blame):
    """
    The reason why an RMA has entered the system for us. The type effects how it is handled in the system.
    """
    def save(self, *args, **kwargs):
        if type(self) == RMACause:
            raise AbstractionError("Cannot store superclass RMACause")
        
        super(RMACause, self).save(*args, **kwargs)


class StockRMA(RMACause):
    """
    A broken product in the stock. Just for stock and not for a customer.
    """
    article_type = models.ForeignKey(ArticleType)

    value = MoneyField()

    @transaction.atomic()
    def save(self, *args, **kwargs):
        if self.pk is None:
            articles = Stock.objects.filter(article=self.article_type, labeltype__isnull=True)
            if len(articles) == 0:
                raise StockError("No stock exists to create RMA from.")
            description = "RMA from stock with article {}".format(self.article_type.name)
            # Removes the item from the stock. From here on, it is tracked by the internal RMA
            entry = [{'article': self.article_type,
                      'book_value': articles[0].book_value,
                      'count': 1,
                      'is_in': False}]
            StockChangeSet.construct(description=description, entries=entry, enum=enum['rma'])
            super(StockRMA, self).save()
            ima = InternalRMA(rma_cause=self, user_modified=self.user_created, customer=None)
            ima.save()
        else:
            super(StockRMA, self).save()



class CustomerRMATask(models.Model):
    """
    A task where a customer has a problem with products he bought. This can be result in a number of products that are
    broken and need to be handled. Connects to a receipt.
    """
    # The customer
    customer = models.ForeignKey(Customer)

    handled = models.BooleanField(default=False)

    receipt = models.ForeignKey(Transaction)


class CustomerTaskDescription(Blame):
    """
    A description of the situation of the customer-RMA. Intended as a human readable/writable log.
    """

    customer_rma_task = models.ForeignKey(CustomerRMATask)

    text = models.TextField()

    def __str__(self):
        return self.text


class TestRMA(RMACause):
    """
    An issue for an individual product,
    """

    customer_rma_task = models.ForeignKey(CustomerRMATask)

    transaction_line = models.ForeignKey(TransactionLine)

    state = models.CharField(max_length=3)

    def save(self, **kwargs):
        if isinstance(self.transaction_line, SalesTransactionLine):
            if self.state not in TestRMAState.STATES:
                raise StateError("State {} not is list of valid states for this TestRMA".format(self.state))
            if self.pk is None:
                # You cannot have more active RMAs than there are products sold
                count = 0
                internal_rmas = InternalRMA.objects.filter(rma_cause__transaction_line=self.transaction_line)
                for in_rma in internal_rmas:
                    if in_rma.state in InternalRMAState.OPEN_STATES:
                        count += 1
                # if count >= translinecount then you cannot add a new one
                if count >= self.transaction_line.count:
                    raise RMACountError("You tried to open more active RMAs than there are counts for transaction {}".
                                        format(self.transaction_line))

        # Everything checks out, lets save
        # Consider that we must make an internal RMA for a physical product
        with transaction.atomic():
            if isinstance(self.transaction_line, SalesTransactionLine):
                if self.pk is None:
                    sold_line = self.refund_line.sold_transaction_line
                    if hasattr(sold_line, 'salestransactionline') and sold_line.salestransactionline is not None:
                        internal_rma = InternalRMA(rma_cause=self, customer=self.customer_rma_task.customer,
                                               state=self.state)
                        internal_rma.save()
            super(TestRMA, self).save()


class TestRMAState(ImmutableBlame):
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

    def save(self, **kwargs):
        if self.state not in TestRMAState.STATES:
            raise StateError("State {} not valid for TestRMAState".format(self.state))


class DirectRefundRMA(RMACause):
    """
    A cause for an RMA that happens when a customer is instantly refunded when he returns a (broken) product.
    """

    refund_line = models.ForeignKey(RefundTransactionLine)

    @transaction.atomic()
    def save(self, *args, **kwargs):
        if not hasattr(self, 'refund_line') or self.refund_line is None:
            raise AttributeError("DirectRefundRMA is missing refund_line")
        if self.pk is None:
            sold_line = self.refund_line.sold_transaction_line
            if hasattr(sold_line, 'salestransactionline') and sold_line.salestransactionline is not None:
                irma = InternalRMA(rma_cause=self, customer=None, user_created=self.user_created)
                irma.save()
        super(DirectRefundRMA, self).save()


class InternalRMA(Blame):
    """
    The handling of a broken product on 'our' side. This tracks whether we are credited for a product or it is replaced.
    Not neccesarily a concern for the customer although this means in practice that the customer has to wait for our
    handling of the problem.
    """

    rma_cause = models.ForeignKey(RMACause)

    customer = models.ForeignKey(Customer, null=True)

    state = models.CharField(max_length=3)

    @transaction.atomic()
    def save(self, **kwargs):
        if self.pk is None:
            if not self.state:
                self.state = InternalRMAState.STARTING_STATE
        if self.state not in InternalRMAState.STATES:
            raise StateError("While saving InternalRMA encountered illegal state {}".format(self.state))
        if self.pk is None:
            super(InternalRMA, self).save()
            irs = InternalRMAState(internal_rma=self, state=self.state, user_modified=self.user_created)
            irs.save()
        else:
            super(InternalRMA, self).save()



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
    STARTING_STATE = 'B'

    internal_rma = models.ForeignKey(InternalRMA)

    state = models.CharField(max_length=3)

    def save(self, **kwargs):
        if self.state not in InternalRMAState.STATES:
            raise StateError("While saving InternalRMA encountered illegal state {}".format(self.state))
        super(InternalRMAState, self).save()


class StateError(Exception):
    pass


class RMACountError(Exception):
    pass


class AbstractionError(Exception):
    pass


class StockError(Exception):
    pass


class MatchingException(Exception):
    pass


class AttributeError(Exception):
    pass



from money.models import MoneyField, PriceField, CostField
from stock.stocklabel import StockLabeledLine
from stock.models import StockChangeSet, Id10TError
from article.models import ArticleType
from stock.enumeration import enum
from tools.util import _assert
from swipe.settings import USED_CURRENCY

from django.db import models, transaction


class TransactionLine(models.Model):
    """
    Superclass of transaction line. Contains all the shared information of all transaction line types.
    """
    # A transaction has one or more transaction lines
    transaction = models.ForeignKey("Transaction")
    # What is the id of the SellableType?
    num = models.IntegerField()
    # What did the customer pay for this line?
    price = PriceField()
    # How many are you selling?
    count = models.IntegerField()
    # Is this line refunded yeu?
    isRefunded = models.BooleanField(default=False)
    # Text storage of name of SellableType
    text = models.CharField(max_length=128)


# noinspection PyShadowingBuiltins
class SalesTransactionLine(TransactionLine, StockLabeledLine):
    """
        Equivalent to one stock-modifying line on a Receipt
    """
    # How much did the ArticleType cost?
    cost = CostField()
    # Which ArticleType are we talking about?
    article = models.ForeignKey(ArticleType)

    @staticmethod
    def handle(changes, register_id):
        # Create stockchange
        to_change = []
        for change in changes:
            chan = {"count": change.count, "article": change.article, "is_in": False, "book_value": change.cost}
            to_change.append(chan)
        return StockChangeSet.construct("Register {}".format(register_id), to_change, enum["cash_register"])


class OtherCostTransactionLine(TransactionLine):
    """
        Transaction for a product that has no stock but is orderable.
    """
    @staticmethod
    def handle(changes, register_id):
        pass


class OtherTransactionLine(TransactionLine):
    """
        One transaction-line for a text-specified reason.
    """

    @staticmethod
    def handle(changes, register_id):
        pass


class InactiveError(Exception):
    pass


class Payment(models.Model):
    """
    Single payment for a transaction. The sum of all payments should be equal to the value of the sales of the
    transaction
    """
    # Exhange of money when something is sold to a customer
    transaction = models.ForeignKey("Transaction")
    # An amount and currency the customer pays
    amount = MoneyField()
    # Which payment type is this payment added to?
    payment_type = models.ForeignKey('register.PaymentType')


class Transaction(models.Model):
    """
        General transaction for the use in a sales period. Contains a number of transaction lines that could be any form
        of sales.
    """
    # When did the transaction take place?
    time = models.DateTimeField(auto_now_add=True)
    # Which changes did it cause in the stock?
    stock_change_set = models.ForeignKey(StockChangeSet)
    # The sales period it is connected to
    salesperiod = models.ForeignKey('register.SalesPeriod')

    def save(self, *args, indirect=False, **kwargs):
        if not indirect:
            raise Id10TError("Please use the Transaction.construct function.")
        super(Transaction, self).save(*args, **kwargs)

    @staticmethod
    @transaction.atomic()
    def construct(payments, transaction_lines):
        from register.models import RegisterMaster
        #
        sum_of_payments = None
        trans = Transaction()
        transaction_store = {}
        if not RegisterMaster.sales_period_is_open():
            from register.models import InactiveError
            raise InactiveError("Sales period is closed")

        salesperiod = RegisterMaster.get_open_sales_period()

        from sales.models import transaction_line_types

        # Get all stockchangeset lines
        for transaction_line in transaction_lines:
            key = (key for key, value in transaction_line_types.items() if value == type(transaction_line)).__next__()
            if not transaction_store.get(key, None):
                transaction_store[key] = []
            transaction_store[key].append(transaction_line)

        # Create stockchangeset; here final handling for other types of changesets might be done.
        sl = None
        for key in transaction_store.keys():
            line = transaction_line_types[key].handle(transaction_store[key], trans.id)
            if key == "sales":
                sl = line
        if sl is None:
            sl = StockChangeSet.construct(description="Empty stockchangeset for Receipt", entries=[], enum=0)

        trans.stock_change_set = sl

        # Count payments
        first = True
        for payment in payments:
            if first:
                sum_of_payments = payment.amount
            else:
                sum_of_payments += payment.amount
            first = False

        _assert(not first)

        first = True
        sum2 = None

        # Count sum of transactions
        for transaction_line in transaction_lines:
            if first:
                sum2 = transaction_line.price
            else:
                sum2 += transaction_line.price
            first = False
        # Check Quid pro Quo
        _assert(sum2.currency == sum_of_payments.currency)
        _assert(sum2.currency.iso == USED_CURRENCY)
        _assert(sum2.amount == sum_of_payments.amount)
        _assert(salesperiod)

        # save all data
        trans.salesperiod = salesperiod
        trans.save(indirect=True)
        for payment in payments:
            payment.transaction = trans
            payment.save()

        for transaction_line in transaction_lines:
            transaction_line.transaction = trans
            transaction_line.save()
        return trans


# List of all types of transaction lines
transaction_line_types = {"sales": SalesTransactionLine, "other_cost": OtherCostTransactionLine,
                          "other": OtherTransactionLine}

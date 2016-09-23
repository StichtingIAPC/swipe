from money.models import MoneyField, PriceField, CostField
from stock.stocklabel import StockLabeledLine, OrderLabel
from stock.models import StockChangeSet, Id10TError, Stock
from article.models import ArticleType, OtherCostType, SellableType
from stock.enumeration import enum
from tools.util import _assert
from swipe.settings import USED_CURRENCY
from blame.models import Blame, ImmutableBlame
from money.models import Price
from crm.models import User, Customer
from decimal import Decimal
from collections import defaultdict
from order.models import OrderLine
#from typing import List

from django.db import models, transaction


class TransactionLine(Blame):
    """
    Superclass of transaction line. Contains all the shared information of all transaction line types.
    """
    # A transaction has one or more transaction lines
    transaction = models.ForeignKey("Transaction")
    # What is the id of the SellableType(0 for no SellableType)?
    num = models.IntegerField()
    # What did the customer pay for this line?
    price = PriceField()
    # How many are you selling?
    count = models.IntegerField()
    # Is this line refunded yet?
    isRefunded = models.BooleanField(default=False)
    # Text storage of name of SellableType
    text = models.CharField(max_length=128)
    # Reference to order, null if stock
    order = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        if type(self) == TransactionLine:
            raise Id10TError("Cannot instantiate super class TransactionLine. Use specific instead!")
        super(TransactionLine, self).save(*args, **kwargs)


# noinspection PyShadowingBuiltins
class SalesTransactionLine(TransactionLine):
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
    other_cost_type = models.ForeignKey(OtherCostType)
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


class Transaction(Blame):
    """
        General transaction for the use in a sales period. Contains a number of transaction lines that could be any form
        of sales.
    """
    # The sales period it is connected to
    salesperiod = models.ForeignKey('register.SalesPeriod')
    # Customer. Null for anonymous customer
    customer = models.ForeignKey(Customer, null=True)

    def save(self, *args, indirect=False, **kwargs):
        if not indirect:
            raise Id10TError("Please use the Transaction.construct function.")
        super(Transaction, self).save(*args, **kwargs)

    @staticmethod
    def create_transaction(user: User, payments, transaction_lines,
                           customer=None):
        """
        Creates a transaction with the necessary information. Checks stock and payment assertions. The transactionLines provided
        will be checked and modified until they are in such a state that they can be saved.
        :param user: The user which handled the Transaction
        :param payments: List[Payment]. A list of payments to pay for the products. Must match the prices.
        :param transaction_lines: List[TransactionLine]. A list if TransactionLines. It is important to supply at least the
        following information for each TransactionLine:
        - All: price, count, order
        - SalesTransactionLine: article
        - OtherCostTransactionLine: other_cost_type
        - OtherTransactionLine:
        :param customer: A Customer
        :return:
        """
        # Basic assertions
        _assert(isinstance(user, User))
        _assert(customer is None or isinstance(customer, Customer))
        for payment in payments:
            _assert(isinstance(payment, Payment))
        for tr_line in transaction_lines:
            tp = type(tr_line)
            if not (tp == SalesTransactionLine or tp == OtherCostTransactionLine or
                    tp == OtherTransactionLine):
                raise UnimplementedError("Only SalesTransactionLine, OtherCostTransactionLine"
                                         " and OtherTransactionLine are implemented")

        # Early fail for closed sales period
        from register.models import RegisterMaster
        if not RegisterMaster.sales_period_is_open():
            from register.models import InactiveError
            raise InactiveError("Sales period is closed")

        salesperiod = RegisterMaster.get_open_sales_period()

        ILLEGAL_ORDER_REFERENCE = -1 # Primary key chosen in such a way that it is never chosen

        # Now some stock checks
        # Build up supply
        stock_level_dict = {}
        for tr_line in transaction_lines:
            if type(tr_line) == SalesTransactionLine:
                ordr = tr_line.order
                if ordr is None:
                    order_reference = ILLEGAL_ORDER_REFERENCE
                else:
                    order_reference = ordr
                st = stock_level_dict.get((order_reference, tr_line.article), None)
                if not st:
                    stock_level_dict[(order_reference, tr_line.article)] = tr_line.count
                else:
                    stock_level_dict[(order_reference, tr_line.article)] += tr_line.count



        # Checks if there is enough stock
        ORDER_POSITION = 0
        ARTICLE_TYPE_POSITION = 1
        for key in stock_level_dict.keys():
            # Checks for stock level, no order
            if key[ORDER_POSITION] == ILLEGAL_ORDER_REFERENCE:
                arts = Stock.objects.filter(labeltype__isnull=True, article=key[ARTICLE_TYPE_POSITION])
                length = arts.__len__()
                if length == 0:
                    raise NotEnoughStockError("There is no stock without any label for article type {}".format(key[ARTICLE_TYPE_POSITION]))
                elif length > 1:
                    raise UnimplementedError("There are more than two lines for stock of the same label. "
                                             "This shouldn't be happening.")
                else:
                    if arts[0].count < stock_level_dict[key]:
                        raise NotEnoughStockError("ArticleType {} has {} in stock but there is demand for {}".
                                                  format(key[ARTICLE_TYPE_POSITION], arts[0].count, stock_level_dict[key]))
                # Assumes unity of all stock with same label. If this is not true, break
                _assert(arts[0].count >= stock_level_dict[key])
            else:
                arts = Stock.objects.filter(labeltype__isnull=OrderLabel, labelkey=key[ORDER_POSITION],
                                            article=key[ARTICLE_TYPE_POSITION])
                length = arts.__len__()
                if length == 0:
                    raise NotEnoughStockError("There is no stock for order {} for article type {}".format(key[ORDER_POSITION],
                                              key[ARTICLE_TYPE_POSITION]))
                elif length > 1:
                    raise UnimplementedError("There are more than two lines for stock of the same label. "
                                             "This shouldn't be happening.")
                else:
                    if arts[0].count < stock_level_dict[key]:
                        raise NotEnoughStockError("ArticleType {} has {} in stock but there is demand for {} in order {}".
                                                  format(key[ARTICLE_TYPE_POSITION], arts[0].count,
                                                         stock_level_dict[key], key[ORDER_POSITION]))
        # If the interpreter is here, it means there are no problems with the stock.
        # Test payments
        should_be_paid = defaultdict(lambda: 0)
        for tr_line in transaction_lines:
            curr = tr_line.price.currency
            amount = tr_line.price.amount
            count = tr_line.count
            should_be_paid[curr] += amount*count

        is_paid = defaultdict(lambda: 0)
        for payment in payments:
            amt = payment.amount.amount
            curr = payment.amount.currency
            is_paid[curr] += amt

        if len(should_be_paid) != len(is_paid):
            raise PaymentMisMatchError("Number of currencies does not match. Aborting transaction")
        else:
            for key in should_be_paid.keys():
                paid = is_paid.get(key)
                if paid is None:
                    raise PaymentMisMatchError("Payment does not exist for currency {}".format(str(key)))
                else:
                    if should_be_paid[key] != is_paid[key]:
                        raise PaymentMisMatchError("Expected {} for currency {} but got {}".format(should_be_paid[key],
                                                                                                   key, is_paid[key]))

        order_other_cost_count = defaultdict(lambda: 0)
        for tr_line in transaction_lines:
            if type(tr_line) == OtherCostTransactionLine:
                if tr_line.order is not None:
                    OrderLine.objects.filter(wishable_id=tr_line.other_cost_type)



        # We assume everything succeeded, now we construct the stock changes
        change_set = []
        # Transaction lines
        for i in range(0, len(transaction_lines)):
            if type(transaction_lines[i]) == SalesTransactionLine:
                if transaction_lines[i].order is None:
                    stock_line = Stock.objects.get(article=transaction_lines[i].article, labeltype__isnull=True)
                    transaction_lines[i].cost = stock_line.book_value
                    change = {'article': transaction_lines[i].article,
                              'book_value': stock_line.book_value,
                              'count': transaction_lines[i].count,
                              'is_in': False}
                    change_set.append(change)
                else:
                    stock_line = Stock.objects.get(article=transaction_lines[i].article, labeltype=OrderLabel,
                                                   labelkey=transaction_lines[i].order)
                    transaction_lines[i].cost = stock_line.book_value
                    change = {'article': transaction_lines[i].article,
                              'book_value': stock_line.book_value,
                              'count': transaction_lines[i].count,
                              'is_in': False,
                              'label': OrderLabel(transaction_lines[i].order)}
                    change_set.append(change)
                # Set rest of relevant properties for SalesTransactionLine
                transaction_lines[i].num = transaction_lines[i].article.pk
                transaction_lines[i].text = str(transaction_lines[i].article)
            elif type(transaction_lines[i]) == OtherCostTransactionLine:
                transaction_lines[i].num = transaction_lines[i].other_cost_type.pk
                transaction_lines[i].text = str(transaction_lines[i].other_cost_type)
            else:
                _assert(len(transaction_lines[i].text) > 0)
            # Don't forget the user
            transaction_lines[i].user_modified = user


        with transaction.atomic():
            # Final constructions of all related values
            trans = Transaction(salesperiod=salesperiod, customer=customer, user_modified=user)
            trans.save(indirect=True)

            for i in range(0,len(transaction_lines)):
                transaction_lines[i].transaction = trans
                transaction_lines[i].save()

            # The post signal of the StockChangeSet should solve the problems of the OrderLines
            CASH_REGISTER_ENUM = 0
            StockChangeSet.construct(description="Transaction: {}".format(trans.pk), entries=change_set, enum=CASH_REGISTER_ENUM)


# List of all types of transaction lines
transaction_line_types = {"sales": SalesTransactionLine, "other_cost": OtherCostTransactionLine,
                          "other": OtherTransactionLine}


class UnimplementedError(Exception):
    pass


class NotEnoughStockError(Exception):
    pass


class PaymentMisMatchError(Exception):
    pass

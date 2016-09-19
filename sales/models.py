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

from django.db import models, transaction


class TransactionLine(Blame):
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
    # Is this line refunded yet?
    isRefunded = models.BooleanField(default=False)
    # Text storage of name of SellableType
    text = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        if type(self) == TransactionLine:
            raise Id10TError("Cannot instantiate super class TransactionLine. Use specific instead!")
        super(TransactionLine, self).save(*args, **kwargs)


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
    def construct(payments, transaction_lines, user):
        from register.models import RegisterMaster
        #
        sum_of_payments = None
        trans = Transaction()
        transaction_store = {}
        if not RegisterMaster.sales_period_is_open():
            from register.models import InactiveError
            raise InactiveError("Sales period is closed")

        salesperiod = RegisterMaster.get_open_sales_period()

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
        trans.user_modified = user
        trans.save(indirect=True)
        for payment in payments:
            payment.transaction = trans
            payment.save()

        for transaction_line in transaction_lines:
            transaction_line.transaction = trans
            transaction_line.user_modified = user
            transaction_line.save()
        return trans

    @staticmethod
    def create_transaction(user, payments, order_article_type_helpers, customer=None):
        """
        Creates a transaction with the necessary information. Checks stock and payment assertions.
        :param user: The user which handled the Transaction
        :param payments: List[Payment]. A list of payments to pay for the products. Must match the prices.
        :param order_article_type_helpers: List[OrderArticleTypeHelper]
        :param customer: A Customer
        :return:
        """
        # Basic assertions
        _assert(isinstance(user, User))
        _assert(customer is None or isinstance(customer, Customer))
        for payment in payments:
            _assert(isinstance(payment, Payment))
        for oath in order_article_type_helpers:
            _assert(isinstance(oath, OrderSellableTypeHelper))
        # Now some more advanced stock checks
        stock_level_dict = {}
        for oath in order_article_type_helpers:
            if type(oath.sellable_type) == ArticleType:
                st = stock_level_dict.get((oath.order, oath.sellable_type), None)
                if not st:
                    stock_level_dict[(oath.order, oath.sellable_type)] = oath.number
                else:
                    stock_level_dict[(oath.order, oath.sellable_type)] += oath.number
            elif type(oath.sellable_type) == OtherCostType:
                pass
                # Does not matter for stock but needs to be caught
            else:
                raise UnimplementedError("This type is not implemented")
        from register.models import RegisterMaster
        if not RegisterMaster.sales_period_is_open():
            from register.models import InactiveError
            raise InactiveError("Sales period is closed")

        salesperiod = RegisterMaster.get_open_sales_period()

        ORDER_POSITION = 0
        ARTICLE_TYPE_POSITION = 1
        for key in stock_level_dict.keys():
            # Checks for stock level, no order
            if key[ORDER_POSITION] == 0:
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
        for oath in order_article_type_helpers:
            curr = oath.price.currency
            amount = oath.price.amount
            should_be_paid[curr] += amount

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

        # We assume everything succeeded, now we construct the stock changes
        change_set = []
        # A bit hackish, but this is a list of costs for all OrderArticleTypeHelpers, which is necessary in creation
        # Transaction lines
        costs = []
        for oath in order_article_type_helpers:
            if type(oath.sellable_type) == ArticleType:
                if oath.order == 0:
                    # OtherCostTypes don't do stock
                    stock_line = Stock.objects.get(article=oath.sellable_type, labelkey__isnull=True)
                    change = {'article': oath.sellable_type,
                              'book_value': stock_line.book_value,
                              'count': oath.number,
                              'is_in': False}
                    costs.append(stock_line.book_value)
                    change_set.append(change)
                else:
                    stock_line = Stock.objects.get(article=oath.sellable_type, labeltype=OrderLabel, labelkey=oath.order)
                    change = {'article': oath.sellable_type,
                              'book_value': stock_line.book_value,
                              'count': oath.number,
                              'is_in': False,
                              'label': OrderLabel(oath.order)}
                    costs.append(stock_line.book_value)
                    change_set.append(change)
            else:
                costs.append(None)
        # Final constructions of all related values
        trans = Transaction(salesperiod=salesperiod)




class OrderSellableTypeHelper:
    """
    Helper class to create transactions in a standardised manner.
    Indicates from which position from stock to take the items, if applicable.
    """
    # Order, from which the sales takes place. 0 if from stock
    order = 0
    # The sellabletype to be sold
    sellable_type = SellableType
    # Number of items to be sold
    number = 0
    # Price. A price per product paid.
    price = Price(amount=Decimal(0))

    def __init__(self, order, sellable_type, number, price):
        """

        :param order:
        :type order: int
        :param sellable_type:
        :type sellable_type: SellableType
        :param number:
        :type number: int
        :param price:
        :type price: Price
        """
        _assert(isinstance(order, int))
        _assert(isinstance(sellable_type, SellableType))
        _assert(isinstance(number, int))
        _assert(isinstance(price, Price))

        self.order = order
        self.sellable_type = sellable_type
        self.number = number
        self.price = price


# List of all types of transaction lines
transaction_line_types = {"sales": SalesTransactionLine, "other_cost": OtherCostTransactionLine,
                          "other": OtherTransactionLine}


class UnimplementedError(Exception):
    pass


class NotEnoughStockError(Exception):
    pass


class PaymentMisMatchError(Exception):
    pass

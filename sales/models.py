from money.models import MoneyField, PriceField, CostField, AccountingGroup
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

from django.db import models, transaction


class TransactionLine(Blame):
    """
    Superclass of transaction line. Contains all the shared information of all transaction line types.
    """
    # A transaction has one or more transaction lines
    transaction = models.ForeignKey("Transaction")
    # What is the id of the SellableType(0 for no SellableType)?
    num = models.IntegerField()
    # What did the customer pay per single product?
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

    def __str__(self):
        if not hasattr(self, 'transaction') or self.transaction is None:
            trans = "None"
        else:
            trans = self.transaction.pk
        if not hasattr(self,'num') or self.num is None:
            num = "None"
        else:
            num = self.num
        if not hasattr(self, 'price') or self.price is None:
            price = "None"
        else:
            price = str(self.price)
        if not hasattr(self, 'count') or self.count is None:
            count = "None"
        else:
            count = self.count
        if not hasattr(self, 'isRefunded') or self.isRefunded is None:
            refun = "Unset"
        else:
            refun = self.isRefunded
        if not hasattr(self, 'order') or self.order is None:
            ordr = "Unset"
        else:
            ordr = self.order
        return "Transaction: {}, Item_number: {}, " \
               "Count: {}, PricePP: {}, Refunded: {}, Order: {}, Text: {}".format(trans,num, count, price, refun,
                                                                                  ordr, self.text)


# noinspection PyShadowingBuiltins
class SalesTransactionLine(TransactionLine):
    """
        Equivalent to one stock-modifying line on a Receipt
    """
    # How much did the ArticleType cost?
    cost = CostField()
    # Which ArticleType are we talking about?
    article = models.ForeignKey(ArticleType)

    def __str__(self):
        prep = super(SalesTransactionLine, self).__str__()
        if not hasattr(self, 'cost') or self.cost is None:
            cost = "None"
        else:
            cost = self.cost
        if not hasattr(self, 'article') or self.article is None:
            art = "None"
        else:
            art = self.article
        return prep + ", Cost: {}, Article: {}".format(cost, art)


class OtherCostTransactionLine(TransactionLine):
    """
        Transaction for a product that has no stock but is orderable.
    """
    other_cost_type = models.ForeignKey(OtherCostType)

    def __str__(self):
        prep = super(OtherCostTransactionLine, self).__str__()
        if not hasattr(self, 'other_cost_type') or self.other_cost_type is None:
            typ = "None"
        else:
            typ = self.other_cost_type
        return prep + ", OtherCostType: {}".format(typ)


class OtherTransactionLine(TransactionLine):
    """
        One transaction-line for a text-specified reason.
    """
    accounting_group = models.ForeignKey(AccountingGroup)

    def __str__(self):
        prep = super(OtherTransactionLine, self).__str__()
        if not hasattr(self, 'accounting_group') or self.accounting_group is None:
            acc = "None"
        else:
            acc = self.accounting_group
        return prep + ", AccountingGroup: {}".format(acc)


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

    def __str__(self):
        if not hasattr(self,'transaction') or self.transaction is None:
            trans = "None"
        else:
            trans = self.transaction
        if not hasattr(self, 'amount') or self.amount is None:
            amt = "None"
        else:
            amt = str(self.amount)
        if not hasattr(self, 'payment_type') or self.payment_type is None:
            ptt = "None"
        else:
            ptt = str(self.payment_type)
        return "Transaction: {}, Amount: {}, PaymentType: {}".format(trans, amt, ptt)


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
        - All: price, count
        - SalesTransactionLine: article, order
        - OtherCostTransactionLine: other_cost_type, order
        - OtherTransactionLine: text
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

        # Now some general checks, including stock checks
        # Build up supply
        stock_level_dict = {}
        for tr_line in transaction_lines:
            _assert(tr_line.count > 0)
            _assert(hasattr(tr_line, 'price') and tr_line.price)
            if type(tr_line) == SalesTransactionLine:
                _assert(hasattr(tr_line, 'article') and tr_line.article)
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
            elif type(tr_line) == OtherTransactionLine:
                # Text is the essential identifier here
                # Accounting group is also needed as to ensure correct VAT and place on turnover list
                _assert(len(tr_line.text) > 0)
                _assert(hasattr(tr_line, 'accounting_group') and tr_line.accounting_group is not None)
            else:
                _assert(hasattr(tr_line, 'other_cost_type') and tr_line.other_cost_type)

        # Checks if there is enough stock
        for key in stock_level_dict.keys():
            order, article = key
            # Checks for stock level, no order
            if order == ILLEGAL_ORDER_REFERENCE:
                arts = Stock.objects.filter(labeltype__isnull=True, article=article)
                length = arts.__len__()
                if length == 0:
                    raise NotEnoughStockError("There is no stock without any label for article type {}".format(article))
                elif length > 1:
                    raise UnimplementedError("There are more than two lines for stock of the same label. "
                                             "This shouldn't be happening.")
                else:
                    if arts[0].count < stock_level_dict[key]:
                        raise NotEnoughStockError("ArticleType {} has {} in stock but there is demand for {}".
                                                  format(article, arts[0].count, stock_level_dict[key]))
                # Assumes unity of all stock with same label. If this is not true, break
                _assert(arts[0].count >= stock_level_dict[key])
            else:
                arts = Stock.objects.filter(labeltype=OrderLabel._labeltype, labelkey=order,
                                            article=article)
                length = arts.__len__()
                if length == 0:
                    raise NotEnoughStockError("There is no stock for order {} for article type {}".format(order,
                                              article))
                elif length > 1:
                    raise UnimplementedError("There are more than two lines for stock of the same label. "
                                             "This shouldn't be happening.")
                else:
                    if arts[0].count < stock_level_dict[key]:
                        raise NotEnoughStockError("ArticleType {} has {} in stock but there is demand for {} in order {}".
                                                  format(article, arts[0].count,
                                                         stock_level_dict[key], order))
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

        # Key is Tuple[order_number, other_cost_type] and stores whether there are enough orderlines for the othercosts.
        # This is not entirely necessary but is a decent sanity check to see if they supplier of the data knows what
        # he is doing.
        order_other_cost_count = defaultdict(lambda: 0)
        for tr_line in transaction_lines:
            if type(tr_line) == OtherCostTransactionLine:
                if tr_line.order is not None:
                    order_other_cost_count[(tr_line.order, tr_line.other_cost_type)] += tr_line.count

        for key in order_other_cost_count.keys():
            order, article = key
            ols = OrderLine.objects.filter(wishable__sellabletype=article, order_id=order)
            if len(ols) < order_other_cost_count[key]:
                raise NotEnoughOrderLinesError("There is are not enough orderlines to transition to sold for Order {} "
                                               "and OtherCostType {}".format(order, article))

        # We assume everything succeeded, now we construct the stock changes
        change_set = []
        # Transaction lines
        for tr_line in transaction_lines:
            if type(tr_line) == SalesTransactionLine:
                if tr_line.order is None:
                    stock_line = Stock.objects.get(article=tr_line.article, labeltype__isnull=True)
                    tr_line.cost = stock_line.book_value
                    change = {'article': tr_line.article,
                              'book_value': stock_line.book_value,
                              'count': tr_line.count,
                              'is_in': False}
                    change_set.append(change)
                else:
                    stock_line = Stock.objects.get(article=tr_line.article, labeltype=OrderLabel._labeltype,
                                                   labelkey=tr_line.order)
                    tr_line.cost = stock_line.book_value
                    change = {'article': tr_line.article,
                              'book_value': stock_line.book_value,
                              'count': tr_line.count,
                              'is_in': False,
                              'label': OrderLabel(tr_line.order)}
                    change_set.append(change)
                # Set rest of relevant properties for SalesTransactionLine
                tr_line.num = tr_line.article.pk
                tr_line.text = str(tr_line.article)
            elif type(tr_line) == OtherCostTransactionLine:
                tr_line.num = tr_line.other_cost_type.pk
                tr_line.text = str(tr_line.other_cost_type)
            else:
                # Symbolic number indicating no related database object
                tr_line.num = -1
            # Don't forget the user
            tr_line.user_modified = user

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

            # Payments
            for payment in payments:
                payment.transaction=trans
                payment.save()

            # Changing the other_costs to sold in their orderlines
            for key in order_other_cost_count.keys():
                ols = OrderLine.objects.filter(wishable__sellabletype=key[1], order_id=key[0])
                for i in range(order_other_cost_count[key]):
                    ols[i].sell(user)


# List of all types of transaction lines
transaction_line_types = {"sales": SalesTransactionLine, "other_cost": OtherCostTransactionLine,
                          "other": OtherTransactionLine}


class UnimplementedError(Exception):
    pass


class NotEnoughStockError(Exception):
    pass


class PaymentMisMatchError(Exception):
    pass


class NotEnoughOrderLinesError(Exception):
    pass

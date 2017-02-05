from collections import defaultdict

from django.db import models, transaction

from article.models import ArticleType, OtherCostType, SellableType
from blame.models import Blame, ImmutableBlame
from crm.models import User, Customer
from money.models import MoneyField, PriceField, CostField, AccountingGroup
from order.models import OrderLine, Order, OrderLineState
from stock.models import StockChangeSet, Id10TError, Stock, StockLock, LockError
from stock.stocklabel import StockLabeledLine, OrderLabel
from pricing.models import PricingModel
from tools.util import raiseif
import customer_invoicing.models


class TransactionLine(Blame):
    """
    Superclass of transaction line. Contains all the shared information of all transaction line types. Creation in the database
    should only be done via the transaction creation function as the checks are done there.
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

    def save(self, **kwargs):
        if type(self) == TransactionLine:
            raise Id10TError("Cannot instantiate super class TransactionLine. Use specific instead!")
        super(TransactionLine, self).save(**kwargs)

    def __str__(self):
        if not hasattr(self, 'transaction') or self.transaction is None:
            trans = "None"
        else:
            trans = self.transaction.pk
        if not hasattr(self, 'num') or self.num is None:
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
               "Count: {}, PricePP: {}, Refunded: {}, Order: {}, Text: {}".format(trans, num, count, price, refun,
                                                                                  ordr, self.text)


# noinspection PyShadowingBuiltins
class SalesTransactionLine(TransactionLine):
    """
        A Transactionline that modifies the stock and uses articles.
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
    # The otherCostType used
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
    # The accounting group to indicate where the money flow should be booked.
    accounting_group = models.ForeignKey(AccountingGroup)

    def __str__(self):
        prep = super(OtherTransactionLine, self).__str__()
        if not hasattr(self, 'accounting_group') or self.accounting_group is None:
            acc = "None"
        else:
            acc = self.accounting_group
        return prep + ", AccountingGroup: {}".format(acc)


class RefundTransactionLine(TransactionLine):
    """
    This a refund of a sold TransactionLine. The sold transaction line that is pointed to, must not be a
    RefundTransactionLine itself. Furthermore, transactionlines cannot be refunded more than they are stored.
    """
    # The transaction line that is already sold.
    sold_transaction_line = models.ForeignKey(TransactionLine, related_name="sold_line")
    # RMA Task from customer to refund. If null, not a refund for an existing test RMA(but could be an RMA)
    test_rma = models.ForeignKey('rma.TestRMA', null=True, default=None)
    # This flag, when True, creates an internal RMA for the product
    creates_rma = models.BooleanField(default=False)

    def __str__(self):
        prep = super(RefundTransactionLine, self).__str__()
        if not hasattr(self, 'transaction_line') or self.transaction_line is None:
            tr = "None"
        else:
            tr = self.transaction_line.pk
        return prep + ", Transaction_number: {}".format(tr)

    def save(self, *args, **kwargs):
        from rma.models import InternalRMA, DirectRefundRMA
        if self.pk is None:
            if hasattr(self, 'test_rma') and self.test_rma is not None:
                raiseif(self.test_rma.pk is None, IncorrectDataException, "Non saved RMA Task")
                self.sold_transaction_line = self.test_rma.transaction_line
                raiseif(self.creates_rma, InvalidDataException, "Cannot be linked to RMA Task and create an RMA")
                self.test_rma.transition('F', self.user_modified)
            if self.creates_rma:
                # If you are here, test_rma is None so there is no danger of collision
                super(RefundTransactionLine, self).save()
                drm = DirectRefundRMA(refund_line=self, user_modified=self.user_modified)
                drm.save()
            else:
                if isinstance(self.sold_transaction_line, SalesTransactionLine):
                    stock_change = [{"article": self.sold_transaction_line.article,
                                     'book_value': self.sold_transaction_line.cost,
                                     # Refunds have a negative count, therefore it should be negated
                                     'count': self.count*-1,
                                     'is_in': True}]
                    StockChangeSet.construct(description="Refund of transactionline "
                                                         "{}".format(self.sold_transaction_line.id),
                                             entries=stock_change, source=StockChangeSet.SOURCE_CASHREGISTER)
                elif hasattr(self.sold_transaction_line, 'salestransactionline'):
                    stock_change = [{"article": self.sold_transaction_line.salestransactionline.article,
                                     'book_value': self.sold_transaction_line.salestransactionline.cost,
                                     # Refunds have a negative count, therefore it should be negated
                                     'count': self.count * -1,
                                     'is_in': True}]
                    StockChangeSet.construct(description="Refund of transactionline "
                                                         "{}".format(self.sold_transaction_line.id),
                                             entries=stock_change, source=StockChangeSet.SOURCE_CASHREGISTER)
                super(RefundTransactionLine, self).save()
        super(RefundTransactionLine, self).save()


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
        if not hasattr(self, 'transaction') or self.transaction is None:
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

    def __str__(self):
        return "SalesPeriodId: {}, CustomerId: {}".format(self.salesperiod_id, self.customer_id)

    def save(self, indirect=False, **kwargs):
        if not indirect:
            raise Id10TError("Please use the Transaction.create_transaction function.")
        super(Transaction, self).save(**kwargs)

    @staticmethod
    def create_transaction(user: User, payments, transaction_lines,
                           customer=None):
        """
        Creates a transaction with the necessary information. Checks stock and payment assertions. The transactionLines
        provided will be checked and modified until they are in such a state that they can be saved.
        :param user: The user which handled the Transaction
        :param payments: List[Payment]. A list of payments to pay for the products. Must match the prices.
        :param transaction_lines: List[TransactionLine]. A list if TransactionLines. It is important to supply at
        least the following information for each TransactionLine:
        - All: price, count
        - SalesTransactionLine: article, order
        - OtherCostTransactionLine: other_cost_type, order
        - OtherTransactionLine: text
        :param customer: A Customer
        :return:
        """
        # Basic assertions
        raiseif(not isinstance(user, User), InvalidDataException, "user is not a User")
        raiseif(customer is not None and not isinstance(customer, Customer),
                InvalidDataException, "customer is not a Customer")
        raiseif(StockLock.is_locked(), LockError, "Stock is locked. Aborting.")

        for payment in payments:
            raiseif(not isinstance(payment, Payment), "payment is not a Payment")
            raiseif(not payment.amount.uses_system_currency(), InvalidDataException, "Payment currency should be system currency")
        types_supported = [SalesTransactionLine, OtherCostTransactionLine, OtherTransactionLine,
                           RefundTransactionLine]
        for tr_line in transaction_lines:
            tp = type(tr_line)
            if tp not in types_supported:
                raise UnimplementedError("Only SalesTransactionLine, OtherCostTransactionLine"
                                         " and OtherTransactionLine are implemented")

        # Early fail for closed sales period
        from register.models import RegisterMaster
        if not RegisterMaster.sales_period_is_open():
            from register.models import InactiveError
            raise InactiveError("Sales period is closed")

        salesperiod = RegisterMaster.get_open_sales_period()

        possible_payment_types = RegisterMaster.get_payment_types_for_open_registers()
        # This boolean checks if a customer invoice needs to be made. If yes, it will pass the needed vars
        # to a function in the customer invoicing module
        transaction_has_invoiced_payment = False

        for payment in payments:
            if payment.payment_type not in possible_payment_types:
                raise PaymentTypeError("Paymenttype: {}, is not in the possible list of payments for the "
                                       "open registers".format(payment.payment_type))
            if payment.payment_type.is_invoicing:
                transaction_has_invoiced_payment = True

        ILLEGAL_ORDER_REFERENCE = -1  # Primary key chosen in such a way that it is never chosen

        # Now some general checks, including stock checks
        # Build up supply
        stock_level_dict = {}
        for tr_line in transaction_lines:
            raiseif(not hasattr(tr_line, 'price') or not tr_line.price, IncorrectDataException, "line.price must exist")
            typ = type(tr_line)
            if typ == SalesTransactionLine:
                raiseif(not hasattr(tr_line, 'article') or not tr_line.article, InvalidDataException,
                        "line.article must exist")
                raiseif(tr_line.count <= 0, InvalidDataException, "There should be more than 1 articles per line")
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
            elif typ == OtherTransactionLine:
                # Text is the essential identifier here
                # Accounting group is also needed as to ensure correct VAT and place on turnover list
                raiseif(len(tr_line.text) <= 0, IncorrectDataException, "line.text must be bigger than 0")
                raiseif(tr_line.count <= 0, IncorrectDataException, "tr_line.count should be more than 0")
                raiseif(not hasattr(tr_line, 'accounting_group') or tr_line.accounting_group is None,
                        InvalidDataException, "OtherTransactionLine should have an accounting group attached")
            elif typ == OtherCostTransactionLine:
                raiseif(tr_line.count <= 0, IncorrectDataException, "line count should be more than 0")
                raiseif(not hasattr(tr_line, 'other_cost_type') or not tr_line.other_cost_type,
                        InvalidDataException, "OtherCostTransactionLine must have other_cost_type linked")
            elif typ == RefundTransactionLine:
                raiseif(tr_line.count >= 0, IncorrectDataException, "line count should be less than 0 for refundlines")
                raiseif(not tr_line.sold_transaction_line.pk,
                        IncorrectDataException, "OtherCostTransactionLine must have a sold_transaction_line attached")

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
                    raise StockModelError("There are more than two lines for stock of the same label. "
                                          "This shouldn't be happening.")
                else:
                    if arts[0].count < stock_level_dict[key]:
                        raise NotEnoughStockError("ArticleType {} has {} in stock but there is demand for {}".
                                                  format(article, arts[0].count, stock_level_dict[key]))
                # Assumes unity of all stock with same label. If this is not true, break
                raiseif(arts[0].count < stock_level_dict[key],
                        NotEnoughStockError, "You are trying to sell too much.")
            else:
                arts = Stock.objects.filter(labeltype=OrderLabel.labeltype, labelkey=order,
                                            article=article)
                length = arts.__len__()
                if length == 0:
                    raise NotEnoughStockError("There is no stock for order {} for article type {}".format(order,
                                              article))
                elif length > 1:
                    raise StockModelError("There are more than two lines for stock of the same label. "
                                          "This shouldn't be happening.")
                else:
                    if arts[0].count < stock_level_dict[key]:
                        raise NotEnoughStockError("ArticleType {} has {} in stock but there is demand "
                                                  "for {} in order {}".format(article, arts[0].count,
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
            ols = OrderLine.objects.filter(wishable__sellabletype=article, order_id=order, state='A')
            if len(ols) < order_other_cost_count[key]:
                raise NotEnoughOrderLinesError("There is are not enough orderlines to transition to sold for Order {} "
                                               "and OtherCostType {}".format(order, article))
        # Now we check if you can truly refund the products you are trying to refund. This means that
        # you do not refund too much when you consider all refunds for a transaction line.
        refund_amount_per_transaction = defaultdict(lambda: 0)
        for tr_line in transaction_lines:
            if type(tr_line) == RefundTransactionLine:
                refund_amount_per_transaction[tr_line.sold_transaction_line] -= tr_line.count

        for key in refund_amount_per_transaction.keys():
            refund_lines = RefundTransactionLine.objects.filter(sold_transaction_line=key)
            accounted_old = 0
            for previous_refunds_on_line in refund_lines:
                accounted_old -= previous_refunds_on_line.count
            accounted_new = refund_amount_per_transaction[key]
            accounted = accounted_new + accounted_old
            amount_sold_in_pointed_transaction = key.count
            if accounted > amount_sold_in_pointed_transaction:
                raise RefundError("Tried to refund {} in addition to previous refunds {} for transactionline {}"
                                  "while only {} were sold for the relevant line.".
                                  format(accounted_new, accounted_old, str(key), amount_sold_in_pointed_transaction))

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
                    stock_line = Stock.objects.get(article=tr_line.article, labeltype=OrderLabel.labeltype,
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
            elif type(tr_line) == OtherTransactionLine:
                # Symbolic number indicating no related database object
                tr_line.num = -1
            elif type(tr_line) == RefundTransactionLine:
                tr_line.text = tr_line.sold_transaction_line.text
                tr_line.num = -1
            # Don't forget the user
            tr_line.user_modified = user

        with transaction.atomic():
            # Final constructions of all related values
            trans = Transaction(salesperiod=salesperiod, customer=customer, user_modified=user)
            trans.save(indirect=True)

            for i in range(0, len(transaction_lines)):
                transaction_lines[i].transaction = trans
                transaction_lines[i].save()

            # The post signal of the StockChangeSet should solve the problems of the OrderLines
            StockChangeSet.construct(description="Transaction: {}".format(trans.pk), entries=change_set,
                                     source=StockChangeSet.SOURCE_CASHREGISTER)

            # Payments
            for payment in payments:
                payment.transaction = trans
                payment.save()

            # Changing the other_costs to sold in their orderlines
            for key in order_other_cost_count.keys():
                ols = list(OrderLine.objects.filter(wishable__sellabletype=key[1], order_id=key[0], state='A'))
                to_sell = order_other_cost_count[key]
                for i in range(to_sell):
                    ols[i].sell(user)

            # Create invoice as it has an invoicing payment type. Handled by customer invoicing module.
            if transaction_has_invoiced_payment:
                customer_invoicing.models.ReceiptCustInvoiceHelper.create_customer_invoice_from_transaction(user, trans,
                                                                                                            payments)


class StockCollections:

    @staticmethod
    def get_stock_with_prices(customer: Customer):
        stock_lines = Stock.objects.filter(labeltype__isnull=True)
        result = []
        for line in stock_lines:
            price = PricingModel.return_price(stock=line, customer=customer)
            result.append((line, price))

        return result

    @staticmethod
    def get_stock_for_customer_with_prices(customer: Customer):
        customer_orders = Order.objects.filter(customer=customer,
                                               orderline__orderlinestate__state__in=OrderLineState.OPEN_STATES).values('id')
        stock_lines = Stock.objects.filter(labeltype__exact="Order", labelkey__in=customer_orders)
        result = []
        for line in stock_lines:
            price = PricingModel.return_price(stock=line, customer=customer)
            result.append((line, price))

        return result


class UnimplementedError(Exception):
    """
    A general error for sales that occurs when the system tries to do something that is not yet
    supported here.
    """
    pass


class NotEnoughStockError(Exception):
    """
    Raised when the system tries to sell more articles than there are on the stock.
    """
    pass


class PaymentMisMatchError(Exception):
    """
    Either too much, too little or the wrong currency was used for paying.
    """
    pass


class PaymentTypeError(Exception):
    """
    Error that indicates a PaymentType was used, that was not connected to any opened register.
    """
    pass


class NotEnoughOrderLinesError(Exception):
    """
    Checks if there are no more othercosts sold from orders, than there are ordered
    """
    pass


class RefundError(Exception):
    """
    Error that indicates an illegal action was done with a RefundTransactionLine
    """
    pass


class StockModelError(Exception):
    """
    Indicates that there are more lines for a stock query than expected. When this happens,
    either the model has changed or something is terribly wrong.
    """
    pass


class InvalidDataException(Exception):
    """
    The data provided was faulty, not the correct types/not enough data
    """
    pass


class IncorrectDataException(Exception):
    """
    The data provided did not match the requirements, was not within bounds.
    """
    pass

from django.contrib.admin import actions
from django.db import models,IntegrityError
from django.db import transaction
from django.utils import timezone
from django.conf import settings

# Create your models here.

from django.utils.translation import ugettext_lazy

from article.models import ArticleType
from money.models import *
from stock.enumeration import enum
from stock.stocklabel import StockLabeledLine
from tools.management.commands.consistencycheck import consistency_check, CRITICAL
from stock.exceptions import Id10TError
from stock.models import StockChange, StockChangeSet
from swipe.settings import  USED_CURRENCY


class PaymentType(models.Model):

    name = models.CharField(max_length=255, unique=True)


class Register(models.Model):
    """
    A register. This can be a cash register with denominations or a virtual register that accepts money
    in a general sense
    """
    name = models.CharField(max_length=255, default="Missing")

    currency = models.ForeignKey(CurrencyData)

    is_cash_register = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    payment_type = models.ForeignKey(PaymentType)

    def get_denominations(self):
        if self.is_cash_register:
            return Denomination.objects.filter(currency=self.currency)
        else:
            return []

    def is_open(self):
        lst = RegisterPeriod.objects.filter(register=self, endTime__isnull=True)
        if len(lst) > 1:
            raise IntegrityError("Register had more than one register period open")
        return len(lst) == 1

    @transaction.atomic
    def open(self, counted_amount, denominations = []):
        if self.is_active:
            if self.is_open():
                raise AlreadyOpenError("Register is already open")
            else:
                if RegisterMaster.sales_period_is_open():
                    open_sales_period = RegisterMaster.get_open_sales_period()

                else:
                    open_sales_period = SalesPeriod()
                    open_sales_period.save()
                register_period = RegisterPeriod(register=self, sales_period=open_sales_period)
                register_period.save()
                if self.is_cash_register:
                    reg_count = RegisterCount(is_opening_count=True, register_period=register_period,amount=counted_amount)
                    reg_count.save(denominations)

                    for denomination in denominations:
                        counted_amount -= denomination.amount*denomination.denomination.amount
                        denomination.register_count=reg_count
                    assert(counted_amount == Decimal("0.00000"))
                    for denomination in denominations:
                        denomination.save()
                else:
                    register_count = RegisterCount(is_opening_count=True, amount=counted_amount)
                    register_count.register_period = register_period
                    register_count.save()

        else:
            raise InactiveError("The register is inactive and cannot be opened")

    def close(self, indirect=False, register_count=False, denomination_counts=False):
        if not indirect:
            raise InvalidOperationError("You can only close a register when the entire sales period is closed")
        else:
            if not self.is_open():
                raise AlreadyClosedError("Register is already closed")
            else:
                reg_period = RegisterPeriod.objects.filter(register=self, endTime__isnull=True)
                if len(reg_period) > 1:
                    raise IntegrityError("More than one register period is open")
                else:
                    reg_per = reg_period.first()
                    reg_per.endTime = reg_per.sales_period.endTime
                    reg_per.save()
                    if not register_count:
                        raise InvalidOperationError("A close without an register count is not accepted.")
                    else:
                        register_count.register_period = reg_per
                        register_count.save(denomination_counts)
                        for denom in denomination_counts:
                            denom.register_count=register_count
                            denom.save()

    def get_current_open_register_period(self):
        if not self.is_open():
            raise InvalidOperationError("Register is not opened")
        return RegisterPeriod.objects.get(register=self, endTime__isnull=True)

    def save(self, **kwargs):
        if self.is_cash_register:
            assert(self.payment_type.name == "Cash")
        super(Register, self).save()

    def __str__(self):
        return "Name: {}, Currency: {}, is_cash_register: {}, is_active: {}, Payment Method: {}".\
            format(self.name, self.currency.name, self.is_cash_register, self.is_active, self.payment_type.name)


class RegisterMaster:
    """
    A helper class that can do the necessary checks to see the state of the registers. Also, some commands can be given
    """

    @staticmethod
    def sales_period_is_open():
        return RegisterMaster.get_open_sales_period()

    @staticmethod
    def get_open_sales_period():
        try:
            a = SalesPeriod.objects.get(endTime__isnull=True)
        except SalesPeriod.DoesNotExist:
            return False
        return a

    @staticmethod
    def number_of_open_registers():
        open_reg_periods = RegisterPeriod.objects.filter(endTime__isnull=True)
        number = len(open_reg_periods)
        if number > 0:
            if not RegisterMaster.sales_period_is_open():
                raise IntegrityError("Registers are open while sales period is closed")
        return number

    @staticmethod
    def get_open_registers():
        return Register.objects.filter(registerperiod__endTime__isnull=True, registerperiod__isnull=False)

    @staticmethod
    def get_payment_types_for_open_registers():
        return PaymentType.objects.filter(register__registerperiod__endTime__isnull=True,
                                          register__registerperiod__isnull=False).distinct()


class ConsistencyChecker:
    """
    Checks the consistency of the system. Will raise IntegrityErrors if the system is an inconsistent state.
    Fixes are required if any of these tests fail
    """

    # This test runs the tests, but rather than raising an error it appends the errors to an array
    @staticmethod
    @consistency_check
    def non_crashing_full_check():
        errors = []
        try:
            ConsistencyChecker.check_open_sales_periods()
        except IntegrityError:
            errors.append({"text": "More than one sales period is open", "location": "SalesPeriods", "line": -1,
                           "severity": CRITICAL})
        try:
            ConsistencyChecker.check_open_register_periods()
        except IntegrityError:
            errors.append({"text": "Register had more than one register period open", "location": "SalesPeriods", "line": -1,"severity": CRITICAL})
        try:
            ConsistencyChecker.check_payment_types()
        except IntegrityError:
            errors.append({"text": "Cash register can only have cash as payment method", "location": "SalesPeriods", "line": -1, "severity": CRITICAL})
        return errors

    @staticmethod
    def full_check():
        ConsistencyChecker.check_open_sales_periods()
        ConsistencyChecker.check_open_register_periods()
        ConsistencyChecker.check_payment_types()

    @staticmethod
    def check_open_sales_periods():
        active_salesperiods = SalesPeriod.objects.filter(endTime__isnull=True)
        if len(active_salesperiods) > 1:
            raise IntegrityError("More than one sales period is open")

    @staticmethod
    def check_open_register_periods():
        active_register_periods = RegisterPeriod.objects.filter(endTime__isnull=True)
        a = {}
        for k in active_register_periods:
            if k.register.id not in a:
                a[k.register.id] = 1
            else:
                raise IntegrityError("Register had more than one register period open")

    @staticmethod
    def check_payment_types():
        registers = Register.objects.all()
        for register in registers:
            if register.is_cash_register and register.payment_type.name != settings.CASH_PAYMENT_TYPE_NAME:
                raise IntegrityError("Cash register can only have cash as payment method")


class SalesPeriod(models.Model):
    """
    A general period in which transactions on opened registers can take place
    """
    beginTime = models.DateTimeField(auto_now_add=True)

    endTime = models.DateTimeField(null=True)

    opening_memo = models.CharField(max_length=255)

    closing_memo = models.CharField(max_length=255)



    @classmethod
    def create(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def is_opened(self):
        return not self.endTime

    @staticmethod
    @transaction.atomic
    def close(registercounts, denominationcounts, memo):
        if RegisterMaster.sales_period_is_open():
            sales_period = RegisterMaster.get_open_sales_period()
            open_registers = RegisterMaster.get_open_registers()
            if not len(registercounts) == len(open_registers):
                raise InvalidOperationError("Not all registers are counted. Aborting close.")
            # Loop over salesperiods and denominationcounts. Check if all things match. If yes, push all transactions.
            reg_periods = RegisterPeriod.objects.filter(endTime__isnull=True)
            # Second check which compares open register periods to open registers. Should always be equals./
            stop = False
            if not len(reg_periods) == len(open_registers):
                raise IntegrityError("Registers open not equal to unstopped register periods. Database inconsistent.")

            # Check if the right registers are counted
            # Also checks the denominations
            for reg_per in reg_periods:
                found = False
                for registercount in registercounts:
                    registercount.is_opening_count = False
                    if registercount.register_period == reg_per:
                        found = True
                        if reg_per.register.is_cash_register:
                            assert registercount.amount >= 0
                            for denom in denominationcounts:
                                if denom.register_count == registercount:
                                    if not reg_per.register.is_cash_register:
                                        raise InvalidOperationError("Denomination count found for non-cash register. Aborting close")
                        break

                if not found:
                    stop = True
                    break

            if stop:
                raise InvalidOperationError("Register counts do not match register periods. Aborting close.")

            sales_period.endTime = timezone.now()

            sales_period.closing_memo = memo


            # Iterates over registers and connects them to the correct register counts.
            # Also adds the correct denomination counts
            for register in open_registers:
                selected_register_count = False
                for registercount in registercounts:
                    if registercount.register_period.register == register:
                        selected_register_count = registercount
                        break
                matching_denom_counts = []
                counted = selected_register_count.amount
                if register.is_cash_register:
                    # Put all denominations for currency in a hashmap
                    #For all denominationcounts
                    for denom in denominationcounts:
                        if denom.register_count == selected_register_count:
                            matching_denom_counts.append(denom)
                            counted = counted - denom.amount*denom.denomination.amount
                assert(counted == Decimal("0.00000"))
                # Saving magic happens after this line
                sales_period.save()
                register.close(indirect=True, register_count=selected_register_count, denomination_counts= matching_denom_counts)
        else:
            raise AlreadyClosedError("Salesperiod is already closed")

    def __str__(self):
        return "Begin time: {}, End time: {}".format(self.beginTime, self.endTime)


class RegisterPeriod(models.Model):
    """
    Opening and closing of a register are administrated here. A register can only be modified if a register is open
    """

    register = models.ForeignKey(Register)

    sales_period = models.ForeignKey(SalesPeriod)

    beginTime = models.DateTimeField(auto_now_add=True)

    endTime = models.DateField(null=True)

    opening_memo = models.CharField(max_length=255)

    closing_memo = models.CharField(max_length=255)

    @classmethod
    def create(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def is_opened(self):
        return not self.endTime

    def __str__(self):
        return "Register_id:{}, Sales_period_id:{}, Begin time:{}, End time: {}".\
            format(self.register.id, self.sales_period.id, self.beginTime, self.endTime)


class RegisterCount(models.Model):
    """
    The amount of currency and perhaps the denomination in the case of a cash register is stored here
    """

    register_period = models.ForeignKey(RegisterPeriod)

    is_opening_count = models.BooleanField()

    amount = models.DecimalField(max_digits=settings.MAX_DIGITS, decimal_places=settings.DECIMAL_PLACES, default=-1.0)

    def save(self, denominations = []):
        register = self.register_period.register
        if register.is_cash_register:
            # Put all denominations for currency in a hashmap
            denoms_for_register = Denomination.objects.filter(currency=register.currency)
            all_denoms = {}
            for denom in denoms_for_register:
                all_denoms[str(denom.amount)] = 1

            #For all denominationcounts
            for denom_count in denominations:
                    # Assert every denomination is available exactly once
                    if (all_denoms.pop(str(denom_count.denomination.amount),0) == 0):
                        raise InvalidDenominationList("Denominations invalid (Unexpected Denom): GOT {}, EXPECTED {}. Crashed at {} || {}".format(denominations, denoms_for_register, denom_count.denomination.amount, all_denoms))

            #Assert every denomination is used
            if (all_denoms.__len__() != 0):
                raise InvalidDenominationList("Denominations invalid: GOT {}, EXPECTED {}".format(denominations, denoms_for_register))
        else:
            assert(not denominations)
        super().save()

    @classmethod
    def create(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def is_cash_register_count(self):
        return self.register_period.register.is_cash_register

    def get_amount_from_denominationcounts(self):
        denom_counts = DenominationCount.objects.filter(register_count=self)
        if len(denom_counts) > 0:
            self.amount = 0.0
            for count in denom_counts:
                self.amount += count.amount
            self.save()

    @staticmethod
    def get_last_register_count_for_register(register):
        if isinstance(register, Register):
            last_register_period = RegisterPeriod.objects.filter(register=register).last("beginTime")
            counts = RegisterCount.objects.filter(register_period=last_register_period)
            if counts.length == 1:
                return counts[0]
            assert (counts.length ==2)
            for count in counts:
                if not count.is_opening_count:
                    return count

        else:
            raise TypeError("Type of register is not Register")

    def __str__(self):
        return "Register_period_id:{}, is_opening_count:{}, Amount:{}".\
            format(self.register_period.id, self.is_opening_count, self.amount)


class DenominationCount(models.Model):
    """
    Counting of the denominations in a cash register
    """
    register_count = models.ForeignKey(RegisterCount)

    denomination = models.ForeignKey(Denomination)

    amount = models.IntegerField()

    @classmethod
    def create(cls, *args, **kwargs):
        return cls(*args, **kwargs)
    def __str__(self):
        return "{} {} x {}".format(self.denomination.currency, self.denomination.amount, self.amount)

class MoneyInOut(models.Model):
    """
    Adds money to a register during an open register period
    """
    register_period = models.ForeignKey(RegisterPeriod)

    amount = models.DecimalField(max_digits=settings.MAX_DIGITS, decimal_places=settings.DECIMAL_PLACES, default=0.0)

    @classmethod
    def create(cls, *args, **kwargs):
        if 'register_period' not in kwargs:
            raise InvalidOperationError("MoneyInOut requires an open register period")
        else:
            register_period = kwargs['register_period']
            if not register_period:
                raise InvalidOperationError("Invalid register period")
            else:
                if not register_period.is_open():
                    InvalidOperationError("Register period should be open")
                else:
                    return cls(*args, **kwargs)

    def __str__(self):
        return "Register Period:{}, Amount:{}".format(self.register_period, self.amount)


class SalesPeriodDifference(models.Model):
    """
    Resolves differences between expected amounts of money in the combined opened registers and the actual amount of money.
    Count is per type of money
    """
    sales_period = models.ForeignKey(SalesPeriod)

    currency_data = models.ForeignKey(CurrencyData)

    amount = models.DecimalField(max_digits=settings.MAX_DIGITS, decimal_places=settings.DECIMAL_PLACES, default=0.0)


class InactiveError(Exception):
    pass


class AlreadyOpenError(Exception):
    pass


class AlreadyClosedError(Exception):
    pass


class InvalidOperationError(Exception):
    pass


class InvalidDenominationList(Exception):
    pass

class Payment(models.Model):
    """
    Single payment for a transaction. The sum of all payments should be equal to the value of the sales of the
    transaction
    """
    transaction = models.ForeignKey("Transaction")
    amount = MoneyField()
    payment_type = models.ForeignKey(PaymentType)


class TransactionLine(models.Model):
    """
    Superclass of transaction line. Contains all the shared information of all transaction line types.
    """
    transaction = models.ForeignKey("Transaction")
    num = models.IntegerField()
    price = PriceField()
    count = models.IntegerField()
    isRefunded = models.BooleanField(default=False)
    text = models.CharField(max_length=128)


class SalesTransactionLine(TransactionLine, StockLabeledLine):
    """
        Equivalent to one stock-modifying line on a Receipt
    """
    cost = CostField()
    article = models.ForeignKey(ArticleType)

    @staticmethod
    def handle(changes, id):
        # Create stockchange
        to_change = []
        for change in changes:
            chan = {"count": change.count, "article": change.article, "is_in": False, "book_value": change.cost}
            to_change.append(chan)
        return StockChangeSet.construct("Register {}".format(id), to_change, enum["cash_register"])


class OtherCostTransactionLine(TransactionLine):
    """
        Transaction for a product that has no stock but is orderable.
    """
    @staticmethod
    def handle(changes):
        pass


class OtherTransactionLine(TransactionLine):
    """
        One transaction-line for a text-specified reason.
    """

    @staticmethod
    def handle(changes):
        pass

# List of all types of transaction lines
transaction_line_types = {"sales": SalesTransactionLine, "other_cost": OtherCostTransactionLine,
                          "other": OtherTransactionLine}


class Transaction(models.Model):
    """
        General transaction for the use in a sales period. Contains a number of transaction lines that could be any form
        of sales.
    """
    time = models.DateTimeField(auto_now_add=True)
    stock_change_set = models.ForeignKey(StockChangeSet)
    salesperiod = models.ForeignKey("SalesPeriod")

    def save(self, *args, indirect=False, **kwargs):
        if not indirect:
            raise Id10TError(
                "Please use the Transaction.construct function.")
        super(Transaction, self).save(*args, **kwargs)

    @staticmethod
    @transaction.atomic()
    def construct(payments, transaction_lines):

        #
        sum_of_payments = None
        trans = Transaction()
        transaction_store = {}
        if not RegisterMaster.sales_period_is_open():
            raise InactiveError("Sales period is closed")

        salesperiod=RegisterMaster.get_open_sales_period()

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
            sl = StockChange.construct(description="Empty stockchangeset for Receipt", entries=[], enum=0)

        trans.stock_change_set = sl

        # Count payments
        first = True
        for payment in payments:
            if first:
                sum_of_payments = payment.amount
            else:
                sum_of_payments += payment.amount
            first = False

        assert(not first)

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
        assert (sum2.currency == sum_of_payments.currency)
        assert(sum2.currency.iso == USED_CURRENCY)
        assert (sum2.amount == sum_of_payments.amount)
        assert salesperiod

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

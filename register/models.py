from django.conf import settings
from django.db import transaction, IntegrityError, models
from django.utils import timezone

from article.models import ArticleType
from money.models import Money, Decimal, Denomination, CurrencyData, Currency, MoneyField
from stock.stocklabel import StockLabeledLine
from sales.models import TransactionLine, Transaction

# Stop PyCharm from seeing tools as a package.
# noinspection PyPackageRequirements
from tools.management.commands.consistencycheck import consistency_check, CRITICAL
from stock.models import StockChange, StockChangeSet
from swipe.settings import CASH_PAYMENT_TYPE_NAME
from tools.util import _assert


class PaymentType(models.Model):
    # Name of the payment type. "Cash" is always used when using cash registers
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return "{}".format(self.name)


class Register(models.Model):
    """
    A register. This can be a cash register with denominations or a virtual register that accepts money
    in a general sense
    """
    # Name of the register. Cosmetic

    class Meta:
        permissions = (
            # Permission to allow linking customers to users via the swipe web interface.
            ("open_register", "Can open a register"),
            ("close_register", "Can close a register"),
        )

    name = models.CharField(max_length=255)
    # Currency used for this register. Unchangeable
    currency = models.ForeignKey(CurrencyData)
    # Indicates if register accepts cash or otherwise is a digital register
    is_cash_register = models.BooleanField(default=False)
    # Do we use this register right now?(Non-active registers should be empty)
    is_active = models.BooleanField(default=True)
    # How do people pay in this register?
    payment_type = models.ForeignKey(PaymentType)

    def get_denominations(self):
        # Gets denominations from register based on its currency
        if self.is_cash_register:
            return Denomination.objects.filter(currency=self.currency)
        else:
            return []

    def is_open(self):
        # Checks if the register is in an opened state
        lst = RegisterPeriod.objects.filter(register=self, endTime__isnull=True)
        if len(lst) > 1:
            raise IntegrityError("Register had more than one register period open")
        return len(lst) == 1

    def get_prev_open_count(self):
        # Get this registers previous count when it was closed.
        # This shouldn't be used for Brief Registers; they should start at zero instead.
        periods = RegisterPeriod.objects.filter(register=self)
        if len(periods) != 0:
            period = periods.last()
            count = RegisterCount.objects.get(register_period=period, is_opening_count=False)
            return Money(Decimal(count.amount), self.currency)
        else:  # Return zero. This prevents Swipe from crashing when a register is opened for the first time.
            return Money(Decimal("0.00000"), self.currency)

    def previous_denomination_count(self):
        # Retrieves the last set of denomination counts which were stored on the last register count
        periods = RegisterPeriod.objects.filter(register=self)
        if len(periods) != 0:
            period = periods.last()
            try:
                count = RegisterCount.objects.get(register_period=period, is_opening_count=False)
            except RegisterCount.DoesNotExist:
                count = RegisterCount.objects.get(register_period=period, is_opening_count=True)
            all_own_denoms = DenominationCount.objects.filter(register_count=count)
            counts = []
            all_denoms = Denomination.objects.filter(currency=self.currency).order_by('amount')
            for denom in all_denoms:
                my_count = 0
                for count in all_own_denoms:
                    if count.denomination.amount == denom.amount:
                        my_count = count.amount
                counts.append(DenominationCount(denomination=denom, amount=my_count))
            return counts

        else:
            denoms = Denomination.objects.filter(currency=self.currency)
            denom_list = []
            for denom in denoms:
                denom_list.append(DenominationCount(denomination=denom, amount=0))
            return denom_list

    @transaction.atomic
    def open(self, counted_amount, memo="", denominations=None):
        # Opens a register, opens a registerperiod if neccessary
        if denominations is None:
            denominations = []

        if memo == "":
            memo = None

        if self.is_active:
            if self.is_open():
                raise AlreadyOpenError("Register is already open")
            else:
                # Calculate Cash Register Difference
                if self.is_cash_register:
                    count = None
                    for denomination in denominations:
                        if count is None:
                            count = denomination.get_money_value()
                        else:
                            count += denomination.get_money_value()
                    diff = count - self.get_prev_open_count()

                # Get or create SalesPeriod
                if RegisterMaster.sales_period_is_open():
                    open_sales_period = RegisterMaster.get_open_sales_period()

                else:
                    open_sales_period = SalesPeriod()
                    open_sales_period.save()

                # Create register_period
                register_period = RegisterPeriod(register=self, sales_period=open_sales_period, memo=memo)
                register_period.save()

                # Create cash register
                if self.is_cash_register:
                    reg_count = RegisterCount(is_opening_count=True, register_period=register_period,
                                              amount=counted_amount)
                    reg_count.save(denominations=denominations)

                    for denomination in denominations:
                        counted_amount -= denomination.amount * denomination.denomination.amount
                        denomination.register_count = reg_count

                    _assert(counted_amount == Decimal("0.00000"))
                    for denomination in denominations:
                        denomination.save()

                else:  # Create Brief Register
                    reg_count = RegisterCount(is_opening_count=True, amount=counted_amount)
                    reg_count.register_period = register_period
                    reg_count.save()

                # Save Register Count Difference
                if self.is_cash_register:
                    # noinspection PyUnboundLocalVariable
                    OpeningCountDifference.objects.create(register_count=reg_count, difference=diff)
        else:
            raise InactiveError("The register is inactive and cannot be opened")

    def close(self, indirect=False, register_count=None, denomination_counts=None):
        # Closes a register, should always be called indirectly via registermaster
        if denomination_counts is None:
            denomination_counts = []

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
                    if register_count is None:
                        raise InvalidOperationError("A close without an register count is not accepted.")
                    else:
                        register_count.register_period = reg_per
                        register_count.save(denominations=denomination_counts)
                        for denom in denomination_counts:
                            denom.register_count = register_count
                            denom.save()

    def get_current_open_register_period(self):
        # Retrieves the current registerperiod if it exists
        if not self.is_open():
            raise InvalidOperationError("Register is not opened")
        return RegisterPeriod.objects.get(register=self, endTime__isnull=True)

    def save(self, **kwargs):
        if self.is_cash_register:
            _assert(self.payment_type.name == CASH_PAYMENT_TYPE_NAME)
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
        # Retrieves the number of open registers, 0 when period is closed and error when inconsistent
        open_reg_periods = RegisterPeriod.objects.filter(endTime__isnull=True)
        number = len(open_reg_periods)
        if number > 0:
            if not RegisterMaster.sales_period_is_open():
                raise IntegrityError("Registers are open while sales period is closed")
        return number

    @staticmethod
    def get_open_registers():
        # Returns all open registers
        return Register.objects.filter(registerperiod__endTime__isnull=True, registerperiod__isnull=False)

    @staticmethod
    def get_payment_types_for_open_registers():
        # Returns the set of payment types that are possible in the open register period
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

            errors.append({
                "text": "More than one sales period is open",
                "location": "SalesPeriods",
                "line": -1,
                "severity": CRITICAL
            })
        try:
            ConsistencyChecker.check_open_register_periods()
        except IntegrityError:
            errors.append({
                "text": "Register had more than one register period open",
                "location": "SalesPeriods",
                "line": -1,
                "severity": CRITICAL
            })
        try:
            ConsistencyChecker.check_payment_types()
        except IntegrityError:
            errors.append({
                "text": "Cash register can only have cash as payment method",
                "location": "SalesPeriods",
                "line": -1,
                "severity": CRITICAL
            })
        return errors

    @staticmethod
    def full_check():
        ConsistencyChecker.check_open_sales_periods()
        ConsistencyChecker.check_open_register_periods()
        ConsistencyChecker.check_payment_types()

    @staticmethod
    def check_open_sales_periods():
        # Checks if there is either one or zero open sales periods
        active_salesperiods = SalesPeriod.objects.filter(endTime__isnull=True)
        if len(active_salesperiods) > 1:
            raise IntegrityError("More than one sales period is open")

    @staticmethod
    def check_open_register_periods():
        # Checks if register is opened at most once
        active_register_periods = RegisterPeriod.objects.filter(endTime__isnull=True)
        a = {}
        for k in active_register_periods:
            if k.register.id not in a:
                a[k.register.id] = 1
            else:
                raise IntegrityError("Register had more than one register period open")

    @staticmethod
    def check_payment_types():
        # Checks for valid payment types. Currently it checks if cash register only hold cash
        registers = Register.objects.all()
        for register in registers:
            if register.is_cash_register and register.payment_type.name != settings.CASH_PAYMENT_TYPE_NAME:
                raise IntegrityError("Cash register can only have cash as payment method")


class SalesPeriod(models.Model):
    """
    A general period in which transactions on opened registers can take place
    """
    # When does the sales period start?
    beginTime = models.DateTimeField(auto_now_add=True)
    # When does the sales period end?(null indicates not ended)
    endTime = models.DateTimeField(null=True)
    # Any relevant information a user wants to add?
    closing_memo = models.CharField(max_length=255, default=None, null=True)

    @classmethod
    def create(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def is_opened(self):
        return not self.endTime

    @staticmethod
    @transaction.atomic
    def close(registercounts, denominationcounts, memo=""):
        # Method of closing the sales period. If the correct registercounts and denominationcounts are added, this
        # method gracefully closes the sales period
        if memo == "":
            memo = None
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
                            _assert(registercount.amount >= 0)
                            for denom in denominationcounts:
                                if denom.register_count == registercount:
                                    if not reg_per.register.is_cash_register:
                                        raise InvalidOperationError("Denomination count found for non-cash register. "
                                                                    "Aborting close")
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
                selected_register_count = None
                for registercount in registercounts:
                    if registercount.register_period.register == register:
                        selected_register_count = registercount
                        break
                matching_denom_counts = []
                counted = selected_register_count.amount
                if register.is_cash_register:
                    # Put all denominations for currency in a hashmap
                    # For all denominationcounts
                    for denom in denominationcounts:
                        if denom.register_count == selected_register_count:
                            matching_denom_counts.append(denom)
                            counted = counted - denom.get_money_value().amount

                    if counted != Decimal("0.00000"):
                        raise InvalidDenominationList("List not equal to expected count: {}, count: {}. "
                                                      "Result: {}".format(matching_denom_counts,
                                                                          selected_register_count, counted))
                # Saving magic happens after this line
                sales_period.save()
                register.close(indirect=True, register_count=selected_register_count,
                               denomination_counts=matching_denom_counts)

            # Calculate register difference
            totals = {}
            for register in open_registers:
                for registercount in registercounts:
                    if registercount.register_period.register == register:
                        opening_count = RegisterCount.objects.filter(register_period=registercount.register_period).first()
                        if totals.get(registercount.register_period.register.currency.iso, None):
                            totals[registercount.register_period.register.currency.iso] += registercount.amount - opening_count.amount

                        else:
                            totals[registercount.register_period.register.currency.iso] = registercount.amount - opening_count.amount

            # Run all transactions
            for transation in Transaction.objects.filter(salesperiod=sales_period):
                for line in TransactionLine.objects.filter(transaction=transation):
                    totals[line.price.currency.iso] -= line.price.amount*line.count

            # Run all MoneyInOuts
            for register in open_registers:
                for registercount in registercounts:
                    if registercount.register_period.register == register:
                        for inout in MoneyInOut.objects.filter(register_period=registercount.register_period):
                            totals[register.currency.iso] += inout.amount

            for currency in totals.keys():
                ClosingCountDifference.objects.create(difference=Money(totals[currency], Currency(currency)),
                                                      sales_period=sales_period)
        else:
            raise AlreadyClosedError("Salesperiod is already closed")

    def __str__(self):
        return "Begin time: {}, End time: {}".format(self.beginTime, self.endTime)


class RegisterPeriod(models.Model):
    """
    Opening and closing of a register are administrated here. A register can only be modified if a register is open
    """
    # Register this period belongs to
    register = models.ForeignKey(Register)
    # A sales period has multiple possible register periods, amongst 'self'
    sales_period = models.ForeignKey(SalesPeriod)
    # When does the register period start?
    beginTime = models.DateTimeField(auto_now_add=True)
    # When does the register period end?(null is not ended)
    endTime = models.DateField(null=True)
    # Any extra information?
    memo = models.CharField(max_length=255, default=None, null=True)

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
    # A register period has one or two counts
    register_period = models.ForeignKey(RegisterPeriod)
    # Indicates if this the opening or the closing count
    is_opening_count = models.BooleanField()
    # How much money is there at the moment of counting?
    amount = models.DecimalField(max_digits=settings.MAX_DIGITS, decimal_places=settings.DECIMAL_PLACES, default=-1.0)

    def save(self, *args, **kwargs):
        denominations = []
        if 'denominations' in kwargs:
            denominations = kwargs['denominations']

        register = self.register_period.register
        if register.is_cash_register:
            # Put all denominations for currency in a hashmap
            denoms_for_register = Denomination.objects.filter(currency=register.currency)
            all_denoms = {}
            for denom in denoms_for_register:
                all_denoms[str(denom.amount)] = 1

            # For all denominationcounts
            for denom_count in denominations:
                    # Assert every denomination is available exactly once
                    if all_denoms.pop(str(denom_count.denomination.amount), 0) == 0:
                        raise InvalidDenominationList("Denominations invalid (Unexpected Denom): GOT {}, EXPECTED {}. "
                                                      "Crashed at {} || {}".format(denominations, denoms_for_register,
                                                                                   denom_count.denomination.amount,
                                                                                   all_denoms))

            # Assert every denomination is used
            if all_denoms.__len__() != 0:
                raise InvalidDenominationList("Denominations invalid: GOT {}, EXPECTED {}".format(denominations,
                                                                                                  denoms_for_register))
        else:
            _assert(not denominations)
        super().save()

    @classmethod
    def create(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def is_cash_register_count(self):
        return self.register_period.register.is_cash_register

    def get_amount_from_denominationcounts(self):
        # Distills an amount value from the denomination counts
        denom_counts = DenominationCount.objects.filter(register_count=self)
        if len(denom_counts) > 0:
            self.amount = 0.0
            for count in denom_counts:
                self.amount += count.amount
            self.save()

    @staticmethod
    def get_last_register_count_for_register(register):
        # Returns last register count for specified register
        if isinstance(register, Register):
            last_register_period = RegisterPeriod.objects.filter(register=register).last("beginTime")
            counts = RegisterCount.objects.filter(register_period=last_register_period)
            if len(counts) == 1:
                return counts[0]
            _assert(len(counts) == 2)
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
    # Every cash register count needs to count all of its denominations, amongst which is 'self'
    register_count = models.ForeignKey(RegisterCount)
    # Denomination belonging to the currency of this register
    denomination = models.ForeignKey(Denomination)
    # Number of pieces of denomination
    amount = models.IntegerField()

    def get_money_value(self):

        return Money(self.denomination.amount, self.denomination.currency) * int(self.amount)

    @classmethod
    def create(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def __str__(self):
        return "{} {} x {}".format(self.denomination.currency, self.denomination.amount, self.amount)


class MoneyInOut(models.Model):
    """
    Adds money to a register during an open register period
    """
    # Period to which the MoneyInOut belongs
    register_period = models.ForeignKey(RegisterPeriod)

    # Positive: ADD, negative: REMOVE moneys
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
    # Period in which there is a difference
    sales_period = models.ForeignKey(SalesPeriod)
    # Currency of the difference
    currency_data = models.ForeignKey(CurrencyData)
    # Amount of difference
    amount = models.DecimalField(max_digits=settings.MAX_DIGITS, decimal_places=settings.DECIMAL_PLACES, default=0.0)


class InactiveError(Exception):
    pass


class AlreadyOpenError(Exception):
    pass


class AlreadyClosedError(Exception):
    pass


class InvalidOperationError(Exception):
    pass


class OpeningCountDifference(models.Model):
    # Difference that can occur when a register is opened. This indicated that money (dis)appeared between closing and
    # opening of the register.
    difference = MoneyField()
    register_count = models.ForeignKey("RegisterCount")

    def __str__(self):
        return "[{}] : {}".format(self.register_count, self.difference)


class ClosingCountDifference(models.Model):
    # Difference that can occur when a sales period closes. Since this could have any reason, it cannot be pointed to
    # a single register. This makes it different from an OpeningCountDifference
    difference = MoneyField()
    sales_period = models.ForeignKey("SalesPeriod")


class InvalidDenominationList(Exception):
    pass

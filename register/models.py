from collections import defaultdict

from django.conf import settings
from django.db import transaction, IntegrityError, models
from django.db.models import Q, Sum

from article.models import ArticleType
from money.models import Money, Decimal, Denomination, CurrencyData, Currency, MoneyField
from sales.models import TransactionLine, Transaction
from stock.models import StockChange, StockChangeSet
from stock.stocklabel import StockLabeledLine
from swipe.settings import CASH_PAYMENT_TYPE_NAME
from tools.management.commands.consistencycheck import consistency_check, CRITICAL
from tools.util import raiseif


class PaymentType(models.Model):
    # Name of the payment type. "Cash" is always used when using cash registers. Should not be changed.
    name = models.CharField(max_length=255, unique=True)
    # Is used for invoicing. If enabled, the cost is to be used at a later date. Should not be changed.
    is_invoicing = models.BooleanField(default=False)

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

    name = models.CharField(max_length=255, unique=True)
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
        sales_period = SalesPeriod.objects.filter(endTime__isnull=True)
        if len(sales_period) > 1:
            raise IntegrityError("More than one salesperiod opened")
        elif len(sales_period) == 1:
            counts = RegisterCount.objects.filter(sales_period=sales_period[0], register=self)
            if len(counts) == 0 or len(counts) > 1:
                return False
            else:
                if counts[0].is_opening_count:
                    return True
                else:
                    raise IntegrityError("The only count for the opened sales period is a closing count")
        else:
            return False

    def get_prev_closing_count(self):
        # Get this registers previous count when it was closed.
        # This shouldn't be used for Brief Registers; they should start at zero instead.
        count_exists = RegisterCount.objects.filter(is_opening_count=False).exists()
        if not count_exists:
            # Dummy the count
            return Money(Decimal("0.00000"), self.currency)
        return RegisterCount.objects.filter(is_opening_count=False).order_by('sales_period__beginTime').last()

    @property
    def denomination_counts(self):
        reg_period_set_count = self.registerperiod_set.count()
        if reg_period_set_count != 0:
            count = self.registerperiod_set.latest().registercount_set.get(
                Q(register_period__endTime=None, is_opening_count=True) |
                Q(register_period__endTime__isnull=False, is_opening_count=False)
            )
            denom_counts = count.denominationcount_set.all()
            counts = []
            for denom in self.currency.denomination_set.all():
                my_count = 0
                for count in denom_counts:
                    if count.denomination == denom:
                        my_count = count.amount
                        break
                counts.append(DenominationCount(denomination=denom, number=my_count))
            return counts
        else:
            denoms = self.currency.denomination_set.all()
            denom_list = []
            for denom in denoms:
                denom_list.append(DenominationCount(denomination=denom, number=0))
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
                    diff = count - self.get_prev_closing_count()

                # Get or create SalesPeriod
                if RegisterMaster.sales_period_is_open():
                    open_sales_period = RegisterMaster.get_open_sales_period()

                else:
                    open_sales_period = SalesPeriod()
                    open_sales_period.save()

                # Create cash register
                if self.is_cash_register:
                    reg_count = RegisterCount(is_opening_count=True, register=self, sales_period=open_sales_period,
                                              amount=counted_amount)
                    reg_count.save(denominations=denominations)

                    for denomination in denominations:
                        counted_amount -= denomination.number * denomination.denomination.amount
                        denomination.register_count = reg_count

                    raiseif(counted_amount != Decimal("0.00000"),
                            RegisterCountError, "denominations amounts did not add up.")
                    for denomination in denominations:
                        denomination.save()

                else:  # Create Brief Register
                    # Optional: Disallow opening with no value
                    reg_count = RegisterCount(is_opening_count=True, amount=counted_amount,
                                              register=self, sales_period=open_sales_period)
                    reg_count.save()

                # Save Register Count Difference
                if self.is_cash_register:
                    # noinspection PyUnboundLocalVariable
                    OpeningCountDifference.objects.create(register_count=reg_count, difference=diff)
        else:
            raise InactiveError("The register is inactive and cannot be opened")

    def close(self, indirect=False, register_count=None, denomination_counts=None):
        """

        :param indirect:
        :param register_count:
        :type register_count: RegisterCount
        :param denomination_counts:
        :type denomination_counts: List[DenominationCount]
        :return:
        """
        # Closes a register, should always be called indirectly via registermaster
        if denomination_counts is None:
            denomination_counts = []

        if not indirect:
            raise InvalidOperationError("You can only close a register when the entire sales period is closed")

        else:
            if not self.is_open():
                raise AlreadyClosedError("Register is already closed")
            else:
                # Opened register means opened sales period
                opened_sales_period = SalesPeriod.get_opened_sales_period()
                reg_count = RegisterCount.objects.filter(register=self, sales_period=opened_sales_period)
                if len(reg_count) > 1:
                    raise IntegrityError("Register is either opened twice or already closed.")
                elif len(reg_count) == 0:
                    raise IntegrityError("Register is apparantly not opened but function indicated that it was.")
                else:
                    if register_count.register_id != self.id:
                        raise InvalidInputError("Registercount's register does not match register")
                    if register_count.is_opening_count or not register_count.sales_period == opened_sales_period:
                        raise InvalidInputError("Registercount should be closing and connected to salesperiod")
                    if not self.is_cash_register:
                        for denom in denomination_counts:
                            raiseif(denom.denomination.currency_id != self.currency_id, InvalidInputError,
                                    "Denomination does not have correct currency")
                            raiseif(denom.register_count.register_id != self.id, InvalidInputError,
                                    "Denominationcount and register don't match")

                    register_count.save()
                    for denom in denomination_counts:
                        denom.save()

    def save(self, **kwargs):
        if self.is_cash_register:
            raiseif(self.payment_type.name != CASH_PAYMENT_TYPE_NAME, CurrencyTypeMismatchError,
                    "Payment type name did not match the provided preset. Use {} instead".format(
                        CASH_PAYMENT_TYPE_NAME))
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
        return RegisterCount.objects.filter(sales_period__endTime__isnull=True, is_opening_count=True).count()

    @staticmethod
    def get_open_registers():
        # Returns all open registers
        return Register.objects.filter(registercount__sales_period__endTime__isnull=False,
                                       registercount__is_opening_count=True).distinct()

    @staticmethod
    def get_payment_types_for_open_registers():
        # Returns the set of payment types that are possible in the open register period
        return PaymentType.objects.filter(register__registercount__sales_period__endTime__isnull=False,
                                          register__registercount__is_opening_count=True).distinct()


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
            ConsistencyChecker.check_open_register_counts()
        except IntegrityError:
            errors.append({
                "text": "Register has more register counts opened in an opened sales period than possible",
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
        ConsistencyChecker.check_open_register_counts()
        ConsistencyChecker.check_payment_types()

    @staticmethod
    def check_open_sales_periods():
        # Checks if there is either one or zero open sales periods
        active_salesperiods = SalesPeriod.objects.filter(endTime__isnull=True)
        if len(active_salesperiods) > 1:
            raise IntegrityError("More than one sales period is open")

    @staticmethod
    def check_open_register_counts():
        # Checks if register is opened at most once
        relevant_register_counts = RegisterCount.objects.filter(sales_period__endTime__isnull=True)
        a = set()
        for count in relevant_register_counts:
            if count.register_id in a:
                raise IntegrityError("Register is opened and closed while Sales period is still open")
            else:
                a.add(count.register_id)

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
    def get_opened_sales_period():
        """
        Gets the opened salesperiod. If there is none or there are multiple, Django will throw an exception.
        :return:
        """
        return SalesPeriod.objects.get(endTime__isnull=True)

    @staticmethod
    @transaction.atomic
    def close(
            registercounts_denominationcounts,
            memo: str=None):
        """
        Closes a sales period by closing all the opened registers. Requires the totals to be filled in.
        :param registercounts_denominationcounts:
        :type registercounts_denominationcounts: List[Tuple[RegisterCount, List[DenominationCount]]]
        :param memo:
        :return:
        """

        # early return when register is closed
        if not RegisterMaster.sales_period_is_open():
            return [AlreadyClosedError("Salesperiod is already closed")]
        if not memo:
            memo = None  # ensure memo is None when None or "" or otherwise empty string

        open_registers = set(RegisterMaster.get_open_registers())
        unchecked = set(open_registers)
        errors = []

        totals = defaultdict(lambda: Decimal(0))

        for registercount, denominationcounts in registercounts_denominationcounts:
            amount = registercount.amount
            register = registercount.register

            # let's already add the counted amount to the currency so that we don't have to do that later on
            totals[register.currency] += amount

            if register.is_cash_register:
                # check if denominations have valid amounts
                if not denominationcounts:
                    errors.append(InvalidDenominationList(
                        "Register {} should have denomination counts attached, but doesn't.".format(register.name)
                    ))
                    break

                denom_amount = Decimal(0)

                for denom_count in denominationcounts:
                    if denom_count.number < 0:
                        errors.append(NegativeCountError(
                            "Register {} has an invalid denomination count for {}{}".format(
                                register.name,
                                denom_count.denomination.currency,
                                denom_count.denomination.amount,
                            )
                        ))
                        break

                    denom_amount += denom_count.get_money_value().amount

                if denom_amount != amount:
                    errors.append(InvalidDenominationList("List not equal to expected count: {}, count: {}. "
                                                          "Result: {}".format(denominationcounts,
                                                                              registercount, denom_amount)))
                    break

            # now that we're done with checking the register's data, we can pop the register from the list.
            if register in unchecked:
                unchecked.pop(register)
            else:
                errors.append(InvalidOperationError("Register {} is not available in the list of "
                                                    "unchecked registers.".format(register.name)))

        if errors:
            return errors

        if len(unchecked) > 0:
            return [InvalidOperationError("There are some uncounted registers, please count them")]

        sales_period = RegisterMaster.get_open_sales_period()


        # get a totals count for all registers: get all
        totals = TransactionLine.objects.filter(transaction__salesperiod=sales_period).distinct('price_currency')\
            .annotate(price_sum=Sum('price'))\
            .values('price_sum', 'price_currency')

        for price_sum, price_currency in totals:
            totals[price_currency] -= price_sum

        in_outs = MoneyInOut.objects.filter(sales_period=sales_period)


    # @staticmethod
    # @transaction.atomic
    # def close(registercounts, denominationcounts, memo=None):
    #     # Method of closing the sales period. If the correct registercounts and denominationcounts are added, this
    #     # method gracefully closes the sales period
    #     if memo == "":
    #         memo = None
    #     if RegisterMaster.sales_period_is_open():
    #         sales_period = RegisterMaster.get_open_sales_period()
    #         open_registers = RegisterMaster.get_open_registers()
    #         if not len(registercounts) == len(open_registers):
    #             raise InvalidOperationError("Not all registers are counted. Aborting close.")
    #         # Loop over salesperiods and denominationcounts. Check if all things match. If yes, push all transactions.
    #         reg_periods = RegisterPeriod.objects.filter(endTime__isnull=True)
    #         # Second check which compares open register periods to open registers. Should always be equals./
    #         stop = False
    #         if not len(reg_periods) == len(open_registers):
    #             raise IntegrityError("Registers open not equal to unstopped register periods. Database inconsistent.")
    #
    #         # Check if the right registers are counted
    #         # Also checks the denominations
    #         for reg_per in reg_periods:
    #             found = False
    #             for registercount in registercounts:
    #                 registercount.is_opening_count = False
    #                 if registercount.register_period == reg_per:
    #                     found = True
    #                     if reg_per.register.is_cash_register:
    #                         raiseif(registercount.amount < 0, NegativeCountError)
    #                         for denom in denominationcounts:
    #                             if denom.register_count == registercount:
    #                                 if not reg_per.register.is_cash_register:
    #                                     raise InvalidOperationError("Denomination count found for non-cash register. "
    #                                                                 "Aborting close")
    #                     break
    #
    #             if not found:
    #                 stop = True
    #                 break
    #
    #         if stop:
    #             raise InvalidOperationError("Register counts do not match register periods. Aborting close.")
    #
    #         sales_period.endTime = timezone.now()
    #         sales_period.closing_memo = memo
    #
    #
    #         # Calculate register difference
    #         totals = {}
    #         for register in open_registers:
    #             for registercount in registercounts:
    #                 if registercount.register_period.register == register:
    #                     opening_count = RegisterCount.objects.filter(register_period=registercount.register_period)\
    #                         .first()
    #                     if totals.get(registercount.register_period.register.currency.iso, None):
    #                         totals[registercount.register_period.register.currency.iso] += \
    #                             registercount.amount - opening_count.amount
    #
    #                     else:
    #                         totals[registercount.register_period.register.currency.iso] = \
    #                             registercount.amount - opening_count.amount
    #                     break
    #
    #         # Run all transactions
    #         for transation in Transaction.objects.filter(salesperiod=sales_period):
    #             for line in TransactionLine.objects.filter(transaction=transation):
    #                 if not totals.get(line.price.currency.iso):
    #                     raise InvalidOperationError("Currency {}"
    #                                                 " is not found for "
    #                                                 "transaction {}".format(line.price.currency, transation))
    #                 else:
    #                     totals[line.price.currency.iso] -= line.price.amount*line.count
    #
    #         # Run all MoneyInOuts
    #         for register in open_registers:
    #             for registercount in registercounts:
    #                 if registercount.register_period.register == register:
    #                     for inout in MoneyInOut.objects.filter(register_period=registercount.register_period):
    #                         totals[register.currency.iso] -= inout.amount
    #
    #
    #         # Iterates over registers and connects them to the correct register counts.
    #         # Also adds the correct denomination counts
    #         for register in open_registers:
    #             selected_register_count = None
    #             for registercount in registercounts:
    #                 if registercount.register_period.register == register:
    #                     selected_register_count = registercount
    #                     break
    #             matching_denom_counts = []
    #             counted = selected_register_count.amount
    #             if register.is_cash_register:
    #                 # Put all denominations for currency in a hashmap
    #                 # For all denominationcounts
    #                 for denom in denominationcounts:
    #                     if denom.register_count == selected_register_count:
    #                         matching_denom_counts.append(denom)
    #                         counted = counted - denom.get_money_value().amount
    #
    #                 if counted != Decimal("0.00000"):
    #                     raise InvalidDenominationList("List not equal to expected count: {}, count: {}. "
    #                                                   "Result: {}".format(matching_denom_counts,
    #                                                                       selected_register_count, counted))
    #
    #         # Everything works and is checked. Now we can safely store everything
    #
    #         sales_period.save()
    #         # If you recognize this code, you read the lines above
    #         for register in open_registers:
    #             selected_register_count = None
    #             for registercount in registercounts:
    #                 if registercount.register_period.register == register:
    #                     selected_register_count = registercount
    #                     break
    #             matching_denom_counts = []
    #             if register.is_cash_register:
    #                 # Put all denominations for currency in a hashmap
    #                 # For all denominationcounts
    #                 for denom in denominationcounts:
    #                     if denom.register_count == selected_register_count:
    #                         matching_denom_counts.append(denom)
    #
    #             register.close(indirect=True, register_count=selected_register_count,
    #                            denomination_counts=matching_denom_counts)
    #
    #         for currency in totals.keys():
    #             ClosingCountDifference.objects.create(difference=Money(totals[currency], Currency(currency)),
    #                                                   sales_period=sales_period)
    #
    #
    #     else:
    #         raise AlreadyClosedError("Salesperiod is already closed")

    def __str__(self):
        return "Begin time: {}, End time: {}".format(self.beginTime, self.endTime)


# class RegisterPeriod(models.Model):
#     """
#     Opening and closing of a register are administrated here. A register can only be modified if a register is open
#     """
#     # Register this period belongs to
#     register = models.ForeignKey(Register)
#     # A sales period has multiple possible register periods, amongst 'self'
#     sales_period = models.ForeignKey(SalesPeriod)
#     # When does the register period start?
#     beginTime = models.DateTimeField(auto_now_add=True)
#     # When does the register period end?(null is not ended)
#     endTime = models.DateField(null=True)
#     # Any extra information?
#     memo = models.CharField(max_length=255, default=None, null=True)
#
#     @classmethod
#     def create(cls, *args, **kwargs):
#         return cls(*args, **kwargs)
#
#     def is_opened(self):
#         return not self.endTime
#
#     def __str__(self):
#         return "Register_id:{}, Sales_period_id:{}, Begin time:{}, End time: {}".\
#             format(self.register.id, self.sales_period.id, self.beginTime, self.endTime)


class RegisterCount(models.Model):
    """
    The amount of currency and perhaps the denomination in the case of a cash register is stored here
    """
    # A register period has one or two counts
    register = models.ForeignKey(Register)
    # The salesperiod of the count
    sales_period = models.ForeignKey(SalesPeriod)
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
            raiseif(denominations, RegisterInconsistencyError, "non-cash registers should not have denominations")
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
                self.amount += count.get_money_value()
            self.save()

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
    number = models.IntegerField()

    def get_money_value(self):
        return Money(self.denomination.amount, self.denomination.currency) * int(self.number)

    @classmethod
    def create(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def __str__(self):
        return "{} {} x {}".format(self.denomination.currency, self.denomination.amount, self.number)


class MoneyInOut(models.Model):
    """
    Adds money to a register during an open register period
    """
    # Register to which
    register = models.ForeignKey(Register)
    # Salesperiod where in/out took place
    sales_period = models.ForeignKey(SalesPeriod)
    # Positive: ADD, negative: REMOVE moneys
    amount = models.DecimalField(max_digits=settings.MAX_DIGITS, decimal_places=settings.DECIMAL_PLACES, default=0.0)

    def __str__(self):
        return "Register:{}, Sales Period: {}, Amount:{}".format(self.register_id, self.sales_period_id, self.amount)


class SalesPeriodDifference(models.Model):
    """
    Resolves differences between expected amounts of money in the combined opened registers and the actual
    amount of money. Count is per type of money
    """
    # Period in which there is a difference
    sales_period = models.ForeignKey(SalesPeriod)
    # Currency of the difference
    currency_data = models.ForeignKey(CurrencyData)
    # Amount of difference
    amount = models.DecimalField(max_digits=settings.MAX_DIGITS, decimal_places=settings.DECIMAL_PLACES, default=0.0)


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


class InvalidRegisterError(Exception):
    pass


class CurrencyTypeMismatchError(Exception):
    pass


class NegativeCountError(Exception):
    pass


class RegisterCountError(Exception):
    pass


class RegisterInconsistencyError(Exception):
    pass

class InvalidInputError(Exception):
    pass

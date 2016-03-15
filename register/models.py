from django.contrib.admin import actions
from django.db import models,IntegrityError
from django.utils import timezone
from django.conf import settings

# Create your models here.

from django.utils.translation import ugettext_lazy
from money.models import *



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

    def open(self, register_count=False):
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
                if not register_count:
                    RegisterCount(is_opening_count=True, register_period=register_period).create()
                else:
                    register_count = RegisterCount(register_count)
                    register_count.register_period = register_period
                    register_count.save()

        else:
            raise InactiveError("The register is inactive and cannot be opened")

    def close(self, indirect=False, register_count=False):
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
                        register_count = RegisterCount(is_opening_count=False, register_period=reg_per)
                        register_count.save()
                    else:
                        register_count = RegisterCount(register_count)
                        register_count.register_period = reg_per
                        register_count.save()

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

    @classmethod
    def create(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def is_opened(self):
        return not self.endTime

    @staticmethod
    def close():
        if RegisterMaster.sales_period_is_open():
            sales_period = RegisterMaster.get_open_sales_period()
            sales_period.endTime = timezone.now()
            sales_period.save()
            open_registers = RegisterMaster.get_open_registers()
            for register in open_registers:
                register.close(indirect=True)
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
            last_register_period = RegisterPeriod.objects.filter(register=register).last()
            return RegisterCount.objects.filter(register_period=last_register_period).last()
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


class InactiveError(Exception):
    pass


class AlreadyOpenError(Exception):
    pass


class AlreadyClosedError(Exception):
    pass


class InvalidOperationError(Exception):
    pass
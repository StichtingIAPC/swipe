from django.contrib.admin import actions
from django.db import models,IntegrityError

# Create your models here.
from django.forms import Field

from django.utils.translation import ugettext_lazy
from money.models import *

from swipe.settings import DECIMAL_PLACES, MAX_DIGITS


class Register(models.Model):
    """
    A register. This can be a cash register with denominations or a virtual register that accepts money in a general sense
    """

    currency = models.ForeignKey(CurrencyData)

    is_cash_register = models.BooleanField()

    def get_denominations(self):
        if(self.is_cash_register):
            return Denomination.objects.filter(currency=self.currency)
        else:
            return []


class RegisterManager():
    """
    A helper class that can do the necessary checks to see the state of the registers. Also, some commands can be given
    """

    @staticmethod
    def sales_period_is_open():
        a = SalesPeriod.objects.latest()
        return not a.endTime

    @staticmethod
    def number_of_open_registers():
        open_regs = RegisterPeriod.objects.filter(endTime__isnull=False)
        number = len(open_regs)
        if number > 0:
            if not RegisterManager.sales_period_is_open():
                raise IntegrityError("Registers are open while sales period is closed")
        return number



class ConsistencyChecker():
    """
    Checks the consistency of the system. Will raise IntegrityErrors if the system is an inconsistent state.
    Fixes are required if any of these tests fail
    """

    @staticmethod
    def check_open_sales_periods():
        active_salesperiods = SalesPeriod.objects.filter(endTime__isnull=True)
        if(len(active_salesperiods)>1):
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


class SalesPeriod(models.Model):
    """
    A general period in which transactions on opened registers can take place
    """
    beginTime = models.DateTimeField()

    endTime = models.DateTimeField(null=True)

    def is_opened(self):
        return not self.endTime


class RegisterPeriod(models.Model):
    """
    Opening and closing of a register are administrated here. A register can only be modified if a register is open
    """

    register = models.ForeignKey(Register)

    sales_period = models.ForeignKey(SalesPeriod)

    beginTime = models.DateTimeField()

    endTime = models.DateField(null=True)

    def is_opened(self):
        return not self.endTime


class RegisterCount(models.Model):
    """
    The amount of currency and perhaps the denomination in the case of a cash register is stored here
    """

    register_period = models.ForeignKey(RegisterPeriod)

    is_opening_count = models.BooleanField()

    amount = models.DecimalField(max_digits=MAX_DIGITS,decimal_places=DECIMAL_PLACES)

    def is_cash_register_count(self):
        return self.register_period.register.is_cash_register


class DenominationCount(models.Model):
    """
    Counting of the denominations in a cash register
    """
    register_count = models.ForeignKey(RegisterCount)

    denomination = models.ForeignKey(Denomination)

    amount = models.IntegerField()


class MoneyInOut(models.Model):
    """
    Adds money to a register during an open register period
    """
    register_period = models.ForeignKey(RegisterPeriod)







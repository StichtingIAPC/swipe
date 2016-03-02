from django.db import models

# Create your models here.
from django.forms import Field

from django.utils.translation import ugettext_lazy
from money.models import *

from swipe.settings import DECIMAL_PLACES, MAX_DIGITS


class Register(models.Model):

    currency = models.ForeignKey(CurrencyData)

    is_cash_register = models.BooleanField()


class SalesPeriod(models.Model):

    beginTime = models.DateTimeField()

    endTime = models.DateTimeField(default=Field.null)

    def is_opened(self):
        return self.endTime == Field.null


class RegisterPeriod(models.Model):

    register = models.ForeignKey(Register)

    sales_period = models.ForeignKey(SalesPeriod)

    beginTime = models.DateTimeField()

    endTime = models.DateField(default=Field.null)

    def is_opened(self):
        return self.endTime == Field.null


class RegisterCount(models.Model):

    register_period = models.ForeignKey(RegisterPeriod)

    is_opening_count = models.BooleanField()

    amount = models.DecimalField(max_digits=MAX_DIGITS,decimal_places=DECIMAL_PLACES)

    def is_cash_register_count(self):
        return self.register_period.register.is_cash_register


class DenominationCount(models.Model):

    register_count = models.ForeignKey(RegisterCount)

    denomination = models.ForeignKey(Denomination)

    amount = models.IntegerField()


class MoneyInOut(models.Model):

    register_period = models.ForeignKey(RegisterPeriod)







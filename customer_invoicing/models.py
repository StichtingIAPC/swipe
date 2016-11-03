from django.db import models
from blame.models import Blame
from money.models import MoneyField, Money
from sales.models import Transaction, PriceField
from tools.util import raiseif


class CustInvoice(Blame):

    invoice_name = models.CharField(max_length=255)

    invoice_address = models.CharField(max_length=255)

    invoice_zip_code = models.CharField(max_length=255)

    invoice_city = models.CharField(max_length=255)

    invoice_country = models.CharField(max_length=255)

    to_be_payed = MoneyField()

    paid = MoneyField()

    handled = models.BooleanField()

    def pay(self, amount: Money):
        if self.pk:
            raiseif(not isinstance(amount, Money), IncorrectClassError, "amount should be a Money")
            used_currency = self.to_be_payed.currency()
            if amount.currency() != used_currency:
                raise CurrencyError("Expected currency {} but received")
        else:
            raise IncorrectStateError("You cannot pay an invoice which is not yet saved")


class ReceiptCustInvoice(CustInvoice):

    receipt = models.ForeignKey(Transaction)


class CustomCustInvoice(CustInvoice):
    pass


class CustomInvoiceLine(Blame):

    text = models.CharField(max_length=255)

    price = PriceField()


class IncorrectStateError(Exception):
    pass

class IncorrectClassError(Exception):
    pass

class CurrencyError(Exception):
    pass
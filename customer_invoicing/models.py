from django.db import models
from blame.models import Blame
from money.models import MoneyField, Money
from sales.models import Transaction, PriceField
from tools.util import raiseif
from decimal import Decimal


class CustInvoice(Blame):

    invoice_name = models.CharField(max_length=255)

    invoice_address = models.CharField(max_length=255)

    invoice_zip_code = models.CharField(max_length=255)

    invoice_city = models.CharField(max_length=255)

    invoice_country = models.CharField(max_length=255)

    invoice_email_address = models.CharField(max_length=255)

    to_be_payed = MoneyField()

    paid = MoneyField()

    handled = models.BooleanField(default=False)

    def pay(self, amount: Money):
        if self.pk:
            raiseif(not isinstance(amount, Money), IncorrectClassError, "amount should be a Money")
            used_currency = self.to_be_payed.currency()
            if amount.currency() != used_currency:
                raise CurrencyError("Expected currency {} but received")
            if self.handled:
                raise IncorrectStateError("You cannot pay an invoice that is already handled")
            payment = CustPayment(cust_invoice=self, payment=amount)
            payment.save()
            self.paid = self.paid + amount
            if self.to_be_payed == self.paid:
                self.handled = True
        else:
            raise IncorrectStateError("You cannot pay an invoice which is not yet saved")

    def determine_address_data(self):
        # There is not determined way to extract the needed information about a person from its context. Using a
        # placeholder will suffice for now
        self.invoice_name = "Placeholder_name"
        self.invoice_email_address = "placeholder@inner-mongolia.com"
        
    def save(self, **kwargs):
        if not self.pk:
            raiseif(not self.to_be_payed, SaveError, "You cannot save if there is no payment yet")
            self.determine_address_data()
            if not self.paid:
                self.paid = Money(amount=Decimal("0"), currency=self.to_be_payed.currency())
        else:
            super(CustInvoice, self).save()


class CustPayment(Blame):

    cust_invoice = models.ForeignKey(CustInvoice)

    payment = MoneyField()


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


class SaveError(Exception):
    pass
from django.db import models
from blame.models import Blame
from money.models import MoneyField, Money, Price
from sales.models import Transaction, PriceField
from tools.util import raiseif
from decimal import Decimal
from crm.models import User


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
            self.save()
        else:
            raise IncorrectStateError("You cannot pay an invoice which is not yet saved")

    def determine_address_data(self):
        # There is not determined way to extract the needed information about a person from its context. Using a
        # placeholder will suffice for now
        if not self.invoice_name:
            self.invoice_name = "Placeholder_name"
        if not self.invoice_address:
            self.invoice_address = "Brinkstraat 1"
        if not self.invoice_zip_code:
            self.invoice_zip_code = "1234AB"
        if not self.invoice_city:
            self.invoice_city = "Enschede"
        if not self.invoice_country:
            self.invoice_country = "Taiwan"
        if not self.invoice_email_address:
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

    @staticmethod
    def create_custom_invoice(invoice_name: str, invoice_address: str, invoice_zip_code: str,
                              invoice_city: str, invoice_country: str, invoice_email_address: str,
                              text_price_combinations: list, user: User):
        cust = CustomCustInvoice(user_modified=user,
                                 invoice_name=invoice_name, invoice_address=invoice_address,
                                 invoice_zip_code=invoice_zip_code, invoice_city=invoice_city,
                                 invoice_country=invoice_country, invoice_email_address=invoice_email_address)
        lines = []  # Type: list[CustomInvoiceLine]
        for text, price in text_price_combinations:
            raiseif(not isinstance(text, str), IncorrectClassError, "text should be a string")
            raiseif(not isinstance(price, Price), IncorrectClassError, "price should be a Price")
            line = CustomInvoiceLine(text=text, price=price)
            lines.append(line)

        # Now, everything is ok and we can save

        cust.save()
        for line in lines:
            line.custom_invoice = cust
            line.save()


class CustomInvoiceLine(Blame):

    custom_invoice = models.ForeignKey(CustomCustInvoice)

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
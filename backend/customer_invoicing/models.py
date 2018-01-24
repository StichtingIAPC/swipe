from django.db import models
from blame.models import Blame
from money.models import MoneyField, Money, Price
from sales.models import PriceField
from tools.util import raiseif
from decimal import Decimal
from crm.models import User, PersonTypeField, OrganisationTypeField, Customer, PersonTypeFieldValue, \
    OrganisationTypeFieldValue, Person


class CustInvoice(Blame):
    """
    An invoice for a customer. Can either be generated from a receipt, or made from scratch
    """

    invoice_name = models.CharField(max_length=255)

    invoice_address = models.CharField(max_length=255)

    invoice_zip_code = models.CharField(max_length=255)

    invoice_city = models.CharField(max_length=255)

    invoice_country = models.CharField(max_length=255)

    invoice_email_address = models.CharField(max_length=255)

    to_be_paid = MoneyField()

    paid = MoneyField()

    handled = models.BooleanField(default=False)

    def pay(self, amount: Money, user: User):
        if self.pk:
            raiseif(not isinstance(amount, Money), IncorrectClassError, "amount should be a Money")
            used_currency = self.to_be_paid.currency
            if amount.currency != used_currency:
                raise CurrencyError("Expected currency {} but received {}".format(used_currency, amount.currency))
            if self.handled:
                raise IncorrectStateError("You cannot pay an invoice that is already handled")
            payment = CustPayment(cust_invoice=self, payment=amount, user_modified=user)
            payment.save()
            self.paid = self.paid + amount
            if self.to_be_paid == self.paid:
                self.handled = True
            else:
                self.handled = False
            self.save()
        else:
            raise IncorrectStateError("You cannot pay an invoice which is not yet saved")

    def determine_address_data(self):
        if isinstance(self, ReceiptCustInvoice):

            if isinstance(self.receipt.customer, Person):
                customer = self.receipt.customer  # type: Customer
            else:
                # Contact organisation is a customer but not a queryable organisation
                customer = self.receipt.customer.organisation
            retrieve_from_fields = True
            fields = None
            # Try to see if invoicing data can be pulled from TypeField(Value)s.
            if hasattr(customer, 'person'):
                # Customer is a person. Retrieve PersonTypeFields
                # Check if the InvoiceFieldPerson line already exists, if not create a new one.
                if InvoiceFieldPerson.objects.count() == 1:
                    fields = InvoiceFieldPerson.objects.first()
                elif InvoiceFieldPerson.objects.count() > 1:
                    raise IncorrectStateError("More than one line found for InvoiceFieldPerson, "
                                              "this shouldn't have happened")
                else:
                    InvoiceFieldPerson.objects.create()
                    retrieve_from_fields = False

                if retrieve_from_fields:
                    id_array = fields.to_int_array()
                    vals = PersonTypeFieldValue.objects.filter(object=customer, typefield_id__in=id_array)
            else:
                # Check if the InvoiceFieldOrganisation line already exists, if not create a new one.
                if InvoiceFieldOrganisation.objects.count() == 1:
                    fields = InvoiceFieldOrganisation.objects.first()
                elif InvoiceFieldOrganisation.objects.count() > 1:
                    raise IncorrectStateError("More than one line found for InvoiceFieldOrganisation, "
                                              "this shouldn't have happened")
                else:
                    InvoiceFieldOrganisation.objects.create()
                    retrieve_from_fields = False

                if retrieve_from_fields:
                    id_array = fields.to_int_array()
                    vals = OrganisationTypeFieldValue.objects.filter(object=customer, typefield_id__in=id_array)

            if retrieve_from_fields:
                # Store found values in dict with key the PersonTypeFields that link it to InvoiceField*
                values_dict = {}
                # noinspection PyUnboundLocalVariable
                for elem in vals:
                    values_dict[elem.typefield] = elem

                # Try to set the values of the invoicing data. Get defaults to None if nothing is found in the dict.
                self.invoice_name = values_dict.get(fields.name)
                self.invoice_address = values_dict.get(fields.address)
                self.invoice_zip_code = values_dict.get(fields.zip_code)
                self.invoice_city = values_dict.get(fields.city)
                self.invoice_country = values_dict.get(fields.country)
                self.invoice_email_address = values_dict.get(fields.email_address)

        if not self.invoice_name:
            self.invoice_name = "Placeholder_name"
        if not self.invoice_address:
            self.invoice_address = "Placeholder_address"
        if not self.invoice_zip_code:
            self.invoice_zip_code = "Placeholder_zipcode"
        if not self.invoice_city:
            self.invoice_city = "Placeholder_city"
        if not self.invoice_country:
            self.invoice_country = "Placeholder_country"
        if not self.invoice_email_address:
            self.invoice_email_address = "Placeholder_email"
        
    def save(self, **kwargs):
        if not self.pk:
            self.determine_address_data()
            if not self.paid:
                self.paid = Money(amount=Decimal("0"), currency=self.to_be_paid.currency)
            if self.paid == self.to_be_paid:
                self.handled = True
            else:
                self.handled = False
            super(CustInvoice, self).save()
        else:
            super(CustInvoice, self).save()

    def __str__(self):
        return "Name: {}, Address: {}, Zip code: {}, City: {}, Country: {}, E-mail address: {}\n" \
               "To be paid: {}, Paid: {}".format(self.invoice_name, self.invoice_address, self.invoice_zip_code,
                                                 self.invoice_city, self.invoice_country, self.invoice_email_address,
                                                 self.to_be_paid, self.paid)


class InvoiceFieldPerson(models.Model):
    """
    Fields for invoicing. For persons.
    """
    name = models.ForeignKey(PersonTypeField, null=True, related_name="pers_name", on_delete=models.PROTECT)
    address = models.ForeignKey(PersonTypeField, null=True, related_name="address", on_delete=models.PROTECT)
    zip_code = models.ForeignKey(PersonTypeField, null=True, related_name="zip", on_delete=models.PROTECT)
    city = models.ForeignKey(PersonTypeField, null=True, related_name="city", on_delete=models.PROTECT)
    country = models.ForeignKey(PersonTypeField, null=True, related_name="country", on_delete=models.PROTECT)
    email_address = models.ForeignKey(PersonTypeField, null=True, related_name="email", on_delete=models.PROTECT)

    def to_int_array(self):
        return [self.name_id, self.address_id, self.zip_code_id, self.city_id, self.country_id, self.email_address_id]

    def is_dummy(self):
        return self.name is None and self.address is None and self.zip_code is None and \
               self.city is None and self.country is None and self.email_address is None

    def __str__(self):
        return "Name_id: {}, Address_id: {}, Zip_id: {}, City_id: {}, Country_id: {}, Email_id: {}".format(
            self.name_id, self.address_id, self.zip_code_id, self.city_id, self.country_id, self.email_address_id
        )
        

class InvoiceFieldOrganisation(models.Model):
    """
    Fields for invoicing. For organisations.
    """
    name = models.ForeignKey(OrganisationTypeField, null=True, related_name="org_name", on_delete=models.PROTECT)
    address = models.ForeignKey(OrganisationTypeField, null=True, related_name="address", on_delete=models.PROTECT)
    zip_code = models.ForeignKey(OrganisationTypeField, null=True, related_name="zip", on_delete=models.PROTECT)
    city = models.ForeignKey(OrganisationTypeField, null=True, related_name="city", on_delete=models.PROTECT)
    country = models.ForeignKey(OrganisationTypeField, null=True, related_name="country", on_delete=models.PROTECT)
    email_address = models.ForeignKey(OrganisationTypeField, null=True, related_name="email", on_delete=models.PROTECT)

    def to_int_array(self):
        return [self.name_id, self.address_id, self.zip_code_id, self.city_id, self.country_id, self.email_address_id]

    def is_dummy(self):
        return self.name is None and self.address is None and self.zip_code is None and \
               self.city is None and self.country is None and self.email_address is None


class CustPayment(Blame):
    """
    A payment for an invoice. Can be only a part of the total amount to be paid
    """

    cust_invoice = models.ForeignKey(CustInvoice, on_delete=models.PROTECT)

    payment = MoneyField()


class ReceiptCustInvoice(CustInvoice):
    """
    An invoice that is made when a transaction is done with a paymenttype that invoices.
    """

    receipt = models.ForeignKey("sales.Transaction", on_delete=models.PROTECT)

    def __str__(self):
        return super(ReceiptCustInvoice, self).__str__() + ", Receipt ID: {}".format(self.receipt_id)


class ReceiptCustInvoiceHelper:
    """
    Workaround for circular dependency issue.
    """

    @staticmethod
    def create_customer_invoice_from_transaction(user: User, transaction, payments):
        from sales.models import Transaction
        raiseif(not isinstance(transaction, Transaction), "transaction should be a transaction")

        to_be_paid = Money(amount=Decimal(0), currency=payments[0].amount.currency)
        paid = Money(amount=Decimal(0), currency=payments[0].amount.currency)

        for payment in payments:
            if not payment.payment_type.is_invoicing:
                paid += payment.amount

            to_be_paid += payment.amount

        receipt_cust_invoice = ReceiptCustInvoice(receipt=transaction, paid=paid, to_be_paid=to_be_paid,
                                                  user_modified=user)
        receipt_cust_invoice.save()


class CustomCustInvoice(CustInvoice):
    """
    A self made invoice containing a number of lines with prices.
    """

    @staticmethod
    def create_custom_invoice(invoice_name: str, invoice_address: str, invoice_zip_code: str,
                              invoice_city: str, invoice_country: str, invoice_email_address: str,
                              text_price_combinations: list, user: User):
        cust = CustomCustInvoice(user_modified=user,
                                 invoice_name=invoice_name, invoice_address=invoice_address,
                                 invoice_zip_code=invoice_zip_code, invoice_city=invoice_city,
                                 invoice_country=invoice_country, invoice_email_address=invoice_email_address)
        lines = []  # Type: List[CustomInvoiceLine]
        to_be_paid = Money(amount=Decimal(0), currency=text_price_combinations[0][1].currency)
        for text, price in text_price_combinations:
            raiseif(not isinstance(text, str), IncorrectClassError, "text should be a string")
            raiseif(not isinstance(price, Price), IncorrectClassError, "price should be a Price")
            to_be_paid += Money(amount=price.amount, currency=price.currency)
            line = CustomInvoiceLine(text=text, price=price)
            lines.append(line)

        # Now, everything is ok and we can save
        cust.to_be_paid = to_be_paid
        cust.save()
        for line in lines:
            line.custom_invoice = cust
            line.user_modified = user
            line.save()


class CustomInvoiceLine(Blame):
    """
    A single line on a custom invoice. Contains a description of the cost and includes a price(including VAT)
    """
    # That invoice document
    custom_invoice = models.ForeignKey(CustomCustInvoice, on_delete=models.PROTECT)
    # Description of the sold item
    text = models.CharField(max_length=255)
    # A price
    price = PriceField()


class IncorrectStateError(Exception):
    pass


class IncorrectClassError(Exception):
    pass


class CurrencyError(Exception):
    pass


class SaveError(Exception):
    pass

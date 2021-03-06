from django.test import TestCase
from tools.testing import TestData
from sales.models import Transaction, SalesTransactionLine, Payment, IncorrectDataException
from money.models import Money, Price, Currency
from customer_invoicing.models import ReceiptCustInvoice, CustInvoice, CustomCustInvoice, CustomInvoiceLine, \
    CustPayment, InvoiceFieldPerson, InvoiceFieldOrganisation
from crm.models import PersonTypeField, PersonTypeFieldValue, PersonType, OrganisationTypeField, \
    OrganisationTypeFieldValue, OrganisationType

from decimal import Decimal
from swipe.settings import USED_CURRENCY


# noinspection PyTypeChecker
class CustInvoiceTestReceiptInvoice(TestCase, TestData):

    def setUp(self):
        self.setup_base_data()

    def test_create_invoice_without_customer(self):
        order = self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments()
        SOLD = 3
        # Invoice register
        self.register_4.open(counted_amount=Decimal(0))
        tl_1 = SalesTransactionLine(price=self.price_system_currency_1, count=SOLD, order=order.pk,
                                    article=self.articletype_1)
        money_1 = Money(amount=self.price_system_currency_1.amount * SOLD,
                        currency=self.price_system_currency_1.currency)
        pymnt_1 = Payment(amount=money_1, payment_type=self.paymenttype_invoice)
        with self.assertRaises(IncorrectDataException):
            Transaction.create_transaction(user=self.user_1, transaction_lines=[tl_1], payments=[pymnt_1], customer=None)

    def test_create_invoice_from_transaction_all_invoiced(self):
        order = self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments()
        SOLD = 3
        # Invoice register
        self.register_4.open(counted_amount=Decimal(0))
        tl_1 = SalesTransactionLine(price=self.price_system_currency_1, count=SOLD, order=order.pk,
                                    article=self.articletype_1)
        money_1 = Money(amount=self.price_system_currency_1.amount * SOLD, currency=self.price_system_currency_1.currency)
        pymnt_1 = Payment(amount=money_1, payment_type=self.paymenttype_invoice)
        Transaction.create_transaction(user=self.user_1, transaction_lines=[tl_1], payments=[pymnt_1], customer=self.customer_person_1)

        trans = Transaction.objects.get()
        self.assertEqual(len(CustInvoice.objects.all()), 1)
        receipt_cust_invoice = ReceiptCustInvoice.objects.get()
        self.assertEqual(receipt_cust_invoice.receipt, trans)
        self.assertEqual(receipt_cust_invoice.paid, Money(amount=Decimal(0), currency=self.currency_current))
        self.assertEqual(receipt_cust_invoice.to_be_paid, money_1)
        self.assertFalse(receipt_cust_invoice.handled)

    def test_create_invoice_no_invoicing(self):
        order = self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments()
        # Maestro register
        self.register_3.open(counted_amount=Decimal(0))
        # Invoice register
        self.register_4.open(counted_amount=Decimal(0))
        SOLD = 1
        tl_1 = SalesTransactionLine(price=self.price_system_currency_1, count=SOLD, order=order.pk,
                                    article=self.articletype_1)
        money_1 = Money(amount=self.price_system_currency_1.amount * SOLD, currency=self.price_system_currency_1.currency)
        pymnt_1 = Payment(amount=money_1, payment_type=self.paymenttype_maestro)
        Transaction.create_transaction(user=self.user_1, transaction_lines=[tl_1], payments=[pymnt_1], customer=self.customer_person_1)
        self.assertFalse(CustInvoice.objects.exists())

    def test_create_invoice_mixed_invoice_and_straight_payment(self):
        order = self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments()
        # Maestro register
        self.register_3.open(counted_amount=Decimal(0))
        # Invoice register
        self.register_4.open(counted_amount=Decimal(0))
        SOLD = 1
        price = Price(amount=Decimal("3"), currency=self.currency_current, vat=1)

        tl_1 = SalesTransactionLine(price=price, count=SOLD, order=order.id,
                                    article=self.articletype_1)
        money_1 = Money(amount=Decimal("1"), currency=self.price_system_currency_1.currency)
        pymnt_1 = Payment(amount=money_1, payment_type=self.paymenttype_maestro)
        money_2 = Money(amount=Decimal("2"), currency=self.price_system_currency_1.currency)
        pymnt_2 = Payment(amount=money_2, payment_type=self.paymenttype_invoice)

        Transaction.create_transaction(user=self.user_1, transaction_lines=[tl_1],
                                       payments=[pymnt_1, pymnt_2], customer=self.customer_person_1)

        trans = Transaction.objects.get()
        self.assertEqual(len(CustInvoice.objects.all()), 1)
        receipt_cust_invoice = ReceiptCustInvoice.objects.get()
        self.assertEqual(receipt_cust_invoice.receipt, trans)
        self.assertEqual(receipt_cust_invoice.paid, Money(amount=Decimal("1"), currency=self.currency_current))
        self.assertEqual(receipt_cust_invoice.to_be_paid, Money(amount=Decimal("3"), currency=self.currency_current))
        self.assertFalse(receipt_cust_invoice.handled)


class CustInvoiceTestCustomInvoice(TestCase, TestData):

    def setUp(self):
        self.setup_base_data()

    def test_create_custom_invoice(self):
        invoice_lines = [["USB kabels", self.price_system_currency_1], ["Poolse schoonmaakmiddelen", self.price_systen_currency_2]]
        CustomCustInvoice.create_custom_invoice(invoice_name="Jaap de Steen", invoice_address="Hallenweg 5",
                                                invoice_zip_code="7522NB", invoice_city="Enschede",
                                                invoice_country="Nederland",
                                                invoice_email_address="bestuuur@iapc.utwente.nl",
                                                text_price_combinations=invoice_lines,
                                                user=self.user_1)

        self.assertEqual(len(CustInvoice.objects.all()), 1)
        custom_invoice = CustomCustInvoice.objects.get()
        self.assertEqual(custom_invoice.paid, Money(amount=Decimal("0"), currency=self.currency_current))
        self.assertEqual(custom_invoice.to_be_paid, Money(amount=self.price_system_currency_1.amount + self.price_systen_currency_2.amount,
                                                          currency=self.currency_current))
        self.assertFalse(custom_invoice.handled)
        custom_invoice_lines = CustomInvoiceLine.objects.all()

        self.assertEqual(len(custom_invoice_lines), 2)
        if custom_invoice_lines[0].price.amount == self.price_system_currency_1.amount:
            self.assertTrue(custom_invoice_lines[1].price.amount == self.price_systen_currency_2.amount)
        else:
            self.assertEquals(custom_invoice_lines[0].price.amount, self.price_systen_currency_2.amount)
            self.assertEquals(custom_invoice_lines[1].price.amount, self.price_system_currency_1.amount)

        for line in custom_invoice_lines:
            self.assertEqual(line.custom_invoice, custom_invoice)

    def test_create_custom_invoice_free(self):
        price = Price(amount=Decimal(0), currency=self.currency_eur, vat=1)
        invoice_lines = [["Poolse schoonmaakmiddelen", price]]
        CustomCustInvoice.create_custom_invoice(invoice_name="Jaap de Steen", invoice_address="Hallenweg 5",
                                                invoice_zip_code="7522NB", invoice_city="Enschede",
                                                invoice_country="Nederland",
                                                invoice_email_address="bestuuur@iapc.utwente.nl",
                                                text_price_combinations=invoice_lines,
                                                user=self.user_1)

        self.assertEqual(len(CustInvoice.objects.all()), 1)
        custom_invoice = CustomCustInvoice.objects.get()
        self.assertTrue(custom_invoice.handled)


# noinspection PyTypeChecker
class CustInvoicePayments(TestCase, TestData):

    def setUp(self):
        self.setup_base_data()
        self.current_currency = Currency(USED_CURRENCY)

    def test_payment_all_invoiced_all_paid(self):
        order = self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments()
        SOLD = 1
        # Invoice register
        self.register_4.open(counted_amount=Decimal(0))
        tl_1 = SalesTransactionLine(price=self.price_system_currency_1, count=SOLD, order=order.id,
                                    article=self.articletype_1)
        money_1 = Money(amount=self.price_system_currency_1.amount * SOLD, currency=self.price_system_currency_1.currency)
        pymnt_1 = Payment(amount=money_1, payment_type=self.paymenttype_invoice)
        Transaction.create_transaction(user=self.user_1, transaction_lines=[tl_1], payments=[pymnt_1], customer=self.customer_person_1)

        receipt_cust_invoice = ReceiptCustInvoice.objects.get()
        self.assertFalse(receipt_cust_invoice.handled)
        receipt_cust_invoice.pay(Money(amount=self.price_system_currency_1.amount, currency=self.current_currency), self.user_1)
        self.assertTrue(receipt_cust_invoice.handled)

    def test_payments_all_invoice_partial_payment_too_little(self):
        order = self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments()
        SOLD = 1
        # Invoice register
        self.register_4.open(counted_amount=Decimal(0))
        tl_1 = SalesTransactionLine(price=self.price_system_currency_1, count=SOLD, order=order.id,
                                    article=self.articletype_1)
        money_1 = Money(amount=self.price_system_currency_1.amount * SOLD, currency=self.price_system_currency_1.currency)
        pymnt_1 = Payment(amount=money_1, payment_type=self.paymenttype_invoice)
        Transaction.create_transaction(user=self.user_1, transaction_lines=[tl_1], payments=[pymnt_1], customer=self.customer_person_1)

        receipt_cust_invoice = ReceiptCustInvoice.objects.get()
        self.assertFalse(receipt_cust_invoice.handled)
        receipt_cust_invoice.pay(Money(amount=Decimal("1"), currency=self.current_currency), self.user_1)
        self.assertFalse(receipt_cust_invoice.handled)

    def test_payments_all_invoice_partial_payment_too_much(self):
        order = self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments()
        SOLD = 1
        # Invoice register
        self.register_4.open(counted_amount=Decimal(0))
        tl_1 = SalesTransactionLine(price=self.price_system_currency_1, count=SOLD, order=order.id,
                                    article=self.articletype_1)
        money_1 = Money(amount=self.price_system_currency_1.amount * SOLD, currency=self.price_system_currency_1.currency)
        pymnt_1 = Payment(amount=money_1, payment_type=self.paymenttype_invoice)
        Transaction.create_transaction(user=self.user_1, transaction_lines=[tl_1], payments=[pymnt_1], customer=self.customer_person_1)

        receipt_cust_invoice = ReceiptCustInvoice.objects.get()
        self.assertFalse(receipt_cust_invoice.handled)
        receipt_cust_invoice.pay(Money(amount=Decimal("2"), currency=self.current_currency), self.user_1)
        self.assertFalse(receipt_cust_invoice.handled)

    def test_payments_partial_invoice(self):
        order = self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments()
        # Maestro register
        self.register_3.open(counted_amount=Decimal(0))
        # Invoice register
        self.register_4.open(counted_amount=Decimal(0))
        SOLD = 1
        price = Price(amount=Decimal("3"), currency=self.currency_current, vat=1)

        tl_1 = SalesTransactionLine(price=price, count=SOLD, order=order.id,
                                    article=self.articletype_1)
        money_1 = Money(amount=Decimal("1"), currency=self.current_currency)
        pymnt_1 = Payment(amount=money_1, payment_type=self.paymenttype_maestro)
        money_2 = Money(amount=Decimal("2"), currency=self.current_currency)
        pymnt_2 = Payment(amount=money_2, payment_type=self.paymenttype_invoice)

        Transaction.create_transaction(user=self.user_1, transaction_lines=[tl_1], payments=[pymnt_1, pymnt_2],
                                       customer=self.customer_person_1)
        receipt_invoice = ReceiptCustInvoice.objects.get()
        self.assertFalse(receipt_invoice.handled)
        receipt_invoice.pay(money_2, self.user_1)
        self.assertTrue(receipt_invoice.handled)

    def test_payments_two_payments(self):
        order = self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments()
        SOLD = 1
        # Invoice register
        self.register_4.open(counted_amount=Decimal(0))
        price = Price(amount=Decimal("2"), currency=self.currency_current, vat=1)
        tl_1 = SalesTransactionLine(price=price, count=SOLD, order=order.id,
                                    article=self.articletype_1)
        money_1 = Money(amount=Decimal("2"), currency=self.price_system_currency_1.currency)
        pymnt_1 = Payment(amount=money_1, payment_type=self.paymenttype_invoice)
        Transaction.create_transaction(user=self.user_1, transaction_lines=[tl_1], payments=[pymnt_1], customer=self.customer_person_1)

        receipt_cust_invoice = ReceiptCustInvoice.objects.get()
        self.assertFalse(receipt_cust_invoice.handled)
        receipt_cust_invoice.pay(Money(amount=Decimal("1"), currency=self.currency_current), self.user_1)
        self.assertFalse(receipt_cust_invoice.handled)
        receipt_cust_invoice.pay(Money(amount=Decimal("1"), currency=self.currency_current), self.user_1)
        self.assertTrue(receipt_cust_invoice.handled)
        self.assertEqual(len(CustPayment.objects.all()), 2)


class InvoiceFieldTests(TestCase, TestData):

    def setUp(self):
        self.setup_base_data()

    def test_get_fields_for_customer_passes_through(self):
        # Lots of experimental typefield data
        ptf = PersonTypeField.objects.create(name="FooPersonTypeFieldName")
        ptf2 = PersonTypeField.objects.create(name="BarPersonTypeFieldName")
        pt = PersonType.objects.create(name="FooPersonTypeName")
        pt.typefields.add(ptf)
        pt.typefields.add(ptf2)
        self.customer_person_1.types.add(pt)
        ptfv = PersonTypeFieldValue(value="InvoiceName", typefield=ptf, type=pt, object=self.customer_person_1)
        ptfv.save()
        ptfv2 = PersonTypeFieldValue(value="InvoiceName", typefield=ptf2, type=pt, object=self.customer_person_1)
        ptfv2.save()

        # Create a receipt with relevant customer
        order = self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments()
        SOLD = 1
        # Invoice register
        self.register_4.open(counted_amount=Decimal(0))
        price = Price(amount=Decimal("2"), currency=self.currency_current, vat=1)
        tl_1 = SalesTransactionLine(price=price, count=SOLD, order=order.id,
                                    article=self.articletype_1)
        money_1 = Money(amount=Decimal("2"), currency=self.price_system_currency_1.currency)
        pymnt_1 = Payment(amount=money_1, payment_type=self.paymenttype_invoice)
        Transaction.create_transaction(user=self.user_1, transaction_lines=[tl_1], payments=[pymnt_1],
                                       customer=self.customer_person_1)
        self.assertTrue(InvoiceFieldPerson.objects.get().is_dummy())

    def test_get_fields_for_customers_person_sets_name(self):
        ptf = PersonTypeField.objects.create(name="FooPersonTypeFieldName")
        ptf2 = PersonTypeField.objects.create(name="BarPersonTypeFieldName")
        ptf3 = PersonTypeField.objects.create(name="BazPersonTypeFieldCity")
        pt = PersonType.objects.create(name="FooPersonTypeName")
        pt.typefields.add(ptf)
        pt.typefields.add(ptf2)
        self.customer_person_1.types.add(pt)
        VAR_NAME = "Magnus"
        VAR_CITY = "Ulaan Bator"
        ptfv = PersonTypeFieldValue(value=VAR_NAME, typefield=ptf, type=pt, object=self.customer_person_1)
        ptfv.save()
        ptfv2 = PersonTypeFieldValue(value="Irr data", typefield=ptf2, type=pt, object=self.customer_person_1)
        ptfv2.save()
        ptfv3 = PersonTypeFieldValue(value=VAR_CITY, typefield=ptf3, type=pt, object=self.customer_person_1)
        ptfv3.save()
        InvoiceFieldPerson.objects.create(name=ptf, city=ptf3)

        # Some buying data
        order = self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments()
        SOLD = 1
        self.register_4.open(counted_amount=Decimal(0))
        price = Price(amount=Decimal("2"), currency=self.currency_current, vat=1)
        tl_1 = SalesTransactionLine(price=price, count=SOLD, order=order.id,
                                    article=self.articletype_1)
        money_1 = Money(amount=Decimal("2"), currency=self.price_system_currency_1.currency)
        pymnt_1 = Payment(amount=money_1, payment_type=self.paymenttype_invoice)
        Transaction.create_transaction(user=self.user_1, transaction_lines=[tl_1], payments=[pymnt_1],
                                       customer=self.customer_person_1)
        rec = ReceiptCustInvoice.objects.get()
        self.assertEqual(rec.invoice_name, VAR_NAME)
        self.assertEqual(rec.invoice_city, VAR_CITY)

    def test_get_fields_for_customers_organisation_sets_name(self):
        # Same as test above, but with organisation
        ptf = OrganisationTypeField.objects.create(name="FooPersonTypeFieldName")
        ptf2 = OrganisationTypeField.objects.create(name="BarPersonTypeFieldName")
        ptf3 = OrganisationTypeField.objects.create(name="BazPersonTypeFieldCity")
        pt = OrganisationType.objects.create(name="FooPersonTypeName")
        pt.typefields.add(ptf)
        pt.typefields.add(ptf2)
        self.organisation.types.add(pt)
        VAR_NAME = "Magnus"
        VAR_CITY = "Ulaan Bator"
        ptfv = OrganisationTypeFieldValue(value=VAR_NAME, typefield=ptf, type=pt, object=self.organisation)
        ptfv.save()
        ptfv2 = OrganisationTypeFieldValue(value="Irr data", typefield=ptf2, type=pt, object=self.organisation)
        ptfv2.save()
        ptfv3 = OrganisationTypeFieldValue(value=VAR_CITY, typefield=ptf3, type=pt, object=self.organisation)
        ptfv3.save()
        InvoiceFieldOrganisation.objects.create(name=ptf, city=ptf3)

        # Some buying data
        order = self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments()
        SOLD = 1
        self.register_4.open(counted_amount=Decimal(0))
        price = Price(amount=Decimal("2"), currency=self.currency_current, vat=1)
        tl_1 = SalesTransactionLine(price=price, count=SOLD, order=order.id,
                                    article=self.articletype_1)
        money_1 = Money(amount=Decimal("2"), currency=self.price_system_currency_1.currency)
        pymnt_1 = Payment(amount=money_1, payment_type=self.paymenttype_invoice)
        Transaction.create_transaction(user=self.user_1, transaction_lines=[tl_1], payments=[pymnt_1],
                                       customer=self.customer_contact_organisation)
        rec = ReceiptCustInvoice.objects.get()
        self.assertEqual(rec.invoice_name, VAR_NAME)
        self.assertEqual(rec.invoice_city, VAR_CITY)

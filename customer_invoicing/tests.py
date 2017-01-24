from django.test import TestCase
from tools.testing import TestData
from sales.models import Transaction, SalesTransactionLine, Payment
from money.models import Money, Price, Currency
from customer_invoicing.models import ReceiptCustInvoice, CustInvoice, CustomCustInvoice, CustomInvoiceLine, CustPayment
from decimal import Decimal
from swipe.settings import USED_CURRENCY


class CustInvoiceTestReceiptInvoice(TestCase, TestData):

    def setUp(self):
        self.setup_base_data()

    def test_create_invoice_from_transaction_all_invoiced(self):
        self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments()
        SOLD = 3
        # Invoice register
        self.register_4.open(counted_amount=Decimal(0))
        tl_1 = SalesTransactionLine(price=self.price_system_currency_1, count=SOLD, order=1,
                                    article=self.articletype_1)
        money_1 = Money(amount=self.price_system_currency_1.amount * SOLD, currency=self.price_system_currency_1.currency)
        pymnt_1 = Payment(amount=money_1, payment_type=self.paymenttype_invoice)
        Transaction.create_transaction(user=self.user_1, transaction_lines=[tl_1], payments=[pymnt_1], customer=None)

        trans = Transaction.objects.get()
        self.assertEqual(len(CustInvoice.objects.all()), 1)
        receipt_cust_invoice = ReceiptCustInvoice.objects.get()
        self.assertEqual(receipt_cust_invoice.receipt, trans)
        self.assertEqual(receipt_cust_invoice.paid, Money(amount=Decimal(0), currency=self.currency_eur))
        self.assertEqual(receipt_cust_invoice.to_be_paid, money_1)
        self.assertFalse(receipt_cust_invoice.handled)

    def test_create_invoice_no_invoicing(self):
        self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments()
        # Maestro register
        self.register_3.open(counted_amount=Decimal(0))
        # Invoice register
        self.register_4.open(counted_amount=Decimal(0))
        SOLD = 1
        tl_1 = SalesTransactionLine(price=self.price_system_currency_1, count=SOLD, order=1,
                                    article=self.articletype_1)
        money_1 = Money(amount=self.price_system_currency_1.amount * SOLD, currency=self.price_system_currency_1.currency)
        pymnt_1 = Payment(amount=money_1, payment_type=self.paymenttype_maestro)
        Transaction.create_transaction(user=self.user_1, transaction_lines=[tl_1], payments=[pymnt_1], customer=None)
        self.assertFalse(CustInvoice.objects.exists())

    def test_create_invoice_mixed_invoice_and_straight_payment(self):
        self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments()
        # Maestro register
        self.register_3.open(counted_amount=Decimal(0))
        # Invoice register
        self.register_4.open(counted_amount=Decimal(0))
        SOLD = 1
        price = Price(amount=Decimal("3"), currency=self.currency_eur, vat=1)

        tl_1 = SalesTransactionLine(price=price, count=SOLD, order=1,
                                    article=self.articletype_1)
        money_1 = Money(amount=Decimal("1"), currency=self.price_system_currency_1.currency)
        pymnt_1 = Payment(amount=money_1, payment_type=self.paymenttype_maestro)
        money_2 = Money(amount=Decimal("2"), currency=self.price_system_currency_1.currency)
        pymnt_2 = Payment(amount=money_2, payment_type=self.paymenttype_invoice)

        Transaction.create_transaction(user=self.user_1, transaction_lines=[tl_1],
                                       payments=[pymnt_1, pymnt_2], customer=None)

        trans = Transaction.objects.get()
        self.assertEqual(len(CustInvoice.objects.all()), 1)
        receipt_cust_invoice = ReceiptCustInvoice.objects.get()
        self.assertEqual(receipt_cust_invoice.receipt, trans)
        self.assertEqual(receipt_cust_invoice.paid, Money(amount=Decimal("1"), currency=self.currency_eur))
        self.assertEqual(receipt_cust_invoice.to_be_paid, Money(amount=Decimal("3"), currency=self.currency_eur))
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
        self.assertEqual(custom_invoice.paid, Money(amount=Decimal("0"), currency=self.currency_eur))
        self.assertEqual(custom_invoice.to_be_paid, Money(amount=self.price_system_currency_1.amount + self.price_systen_currency_2.amount,
                                                          currency=self.currency_eur))
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


class CustInvoicePayments(TestCase, TestData):

    def setUp(self):
        self.setup_base_data()
        self.current_currency = Currency(USED_CURRENCY)

    def test_payment_all_invoiced_all_paid(self):
        self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments()
        SOLD = 1
        # Invoice register
        self.register_4.open(counted_amount=Decimal(0))
        tl_1 = SalesTransactionLine(price=self.price_system_currency_1, count=SOLD, order=1,
                                    article=self.articletype_1)
        money_1 = Money(amount=self.price_system_currency_1.amount * SOLD, currency=self.price_system_currency_1.currency)
        pymnt_1 = Payment(amount=money_1, payment_type=self.paymenttype_invoice)
        Transaction.create_transaction(user=self.user_1, transaction_lines=[tl_1], payments=[pymnt_1], customer=None)

        receipt_cust_invoice = ReceiptCustInvoice.objects.get()
        self.assertFalse(receipt_cust_invoice.handled)
        receipt_cust_invoice.pay(Money(amount=self.price_system_currency_1.amount, currency=self.current_currency), self.user_1)
        self.assertTrue(receipt_cust_invoice.handled)

    def test_payments_all_invoice_partial_payment_too_little(self):
        self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments()
        SOLD = 1
        # Invoice register
        self.register_4.open(counted_amount=Decimal(0))
        tl_1 = SalesTransactionLine(price=self.price_system_currency_1, count=SOLD, order=1,
                                    article=self.articletype_1)
        money_1 = Money(amount=self.price_system_currency_1.amount * SOLD, currency=self.price_system_currency_1.currency)
        pymnt_1 = Payment(amount=money_1, payment_type=self.paymenttype_invoice)
        Transaction.create_transaction(user=self.user_1, transaction_lines=[tl_1], payments=[pymnt_1], customer=None)

        receipt_cust_invoice = ReceiptCustInvoice.objects.get()
        self.assertFalse(receipt_cust_invoice.handled)
        receipt_cust_invoice.pay(Money(amount=Decimal("1"), currency=self.current_currency), self.user_1)
        self.assertFalse(receipt_cust_invoice.handled)

    def test_payments_all_invoice_partial_payment_too_much(self):
        self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments()
        SOLD = 1
        # Invoice register
        self.register_4.open(counted_amount=Decimal(0))
        tl_1 = SalesTransactionLine(price=self.price_system_currency_1, count=SOLD, order=1,
                                    article=self.articletype_1)
        money_1 = Money(amount=self.price_system_currency_1.amount * SOLD, currency=self.price_system_currency_1.currency)
        pymnt_1 = Payment(amount=money_1, payment_type=self.paymenttype_invoice)
        Transaction.create_transaction(user=self.user_1, transaction_lines=[tl_1], payments=[pymnt_1], customer=None)

        receipt_cust_invoice = ReceiptCustInvoice.objects.get()
        self.assertFalse(receipt_cust_invoice.handled)
        receipt_cust_invoice.pay(Money(amount=Decimal("2"), currency=self.current_currency), self.user_1)
        self.assertFalse(receipt_cust_invoice.handled)

    def test_payments_partial_invoice(self):
        self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments()
        # Maestro register
        self.register_3.open(counted_amount=Decimal(0))
        # Invoice register
        self.register_4.open(counted_amount=Decimal(0))
        SOLD = 1
        price = Price(amount=Decimal("3"), currency=self.currency_eur, vat=1)

        tl_1 = SalesTransactionLine(price=price, count=SOLD, order=1,
                                    article=self.articletype_1)
        money_1 = Money(amount=Decimal("1"), currency=self.current_currency)
        pymnt_1 = Payment(amount=money_1, payment_type=self.paymenttype_maestro)
        money_2 = Money(amount=Decimal("2"), currency=self.current_currency)
        pymnt_2 = Payment(amount=money_2, payment_type=self.paymenttype_invoice)

        Transaction.create_transaction(user=self.user_1, transaction_lines=[tl_1], payments=[pymnt_1, pymnt_2],
                                       customer=None)
        receipt_invoice = ReceiptCustInvoice.objects.get()
        self.assertFalse(receipt_invoice.handled)
        receipt_invoice.pay(money_2, self.user_1)
        self.assertTrue(receipt_invoice.handled)

    def test_payments_two_payments(self):
        self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments()
        SOLD = 1
        # Invoice register
        self.register_4.open(counted_amount=Decimal(0))
        price = Price(amount=Decimal("2"), currency=self.currency_eur, vat=1)
        tl_1 = SalesTransactionLine(price=price, count=SOLD, order=1,
                                    article=self.articletype_1)
        money_1 = Money(amount=Decimal("2"), currency=self.price_system_currency_1.currency)
        pymnt_1 = Payment(amount=money_1, payment_type=self.paymenttype_invoice)
        Transaction.create_transaction(user=self.user_1, transaction_lines=[tl_1], payments=[pymnt_1], customer=None)

        receipt_cust_invoice = ReceiptCustInvoice.objects.get()
        self.assertFalse(receipt_cust_invoice.handled)
        receipt_cust_invoice.pay(Money(amount=Decimal("1"), currency=self.currency_eur), self.user_1)
        self.assertFalse(receipt_cust_invoice.handled)
        receipt_cust_invoice.pay(Money(amount=Decimal("1"), currency=self.currency_eur), self.user_1)
        self.assertTrue(receipt_cust_invoice.handled)
        self.assertEqual(len(CustPayment.objects.all()), 2)

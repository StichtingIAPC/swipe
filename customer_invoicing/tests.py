from django.test import TestCase
from tools.testing import TestData
from sales.models import Transaction, SalesTransactionLine, Payment
from money.models import Money
from customer_invoicing.models import ReceiptCustInvoice, CustInvoice
from decimal import Decimal


class CustInvoiceTests(TestCase, TestData):

    def setUp(self):
        self.setup_base_data()

    def test_find_invoice(self):
        self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments()
        SOLD = 3
        self.register_4.open(counted_amount=Decimal(0))
        tl_1 = SalesTransactionLine(price=self.price_eur_1, count=SOLD, order=1,
                                    article=self.articletype_1)
        money_1 = Money(amount=self.price_eur_1.amount * SOLD, currency=self.price_eur_1.currency)
        pymnt_1 = Payment(amount=money_1, payment_type=self.paymenttype_invoice)
        Transaction.create_transaction(user=self.user_1, transaction_lines=[tl_1], payments=[pymnt_1], customer=None)
        self.assertEqual(len(CustInvoice.objects.all()), 1)
        receipt_cust_invoice = ReceiptCustInvoice.objects.get()




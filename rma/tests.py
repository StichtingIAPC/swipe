from django.test import TestCase
from tools.testing import TestData
from rma.models import CustomerRMATask, RMACause, AbstractionError, StockRMA, InternalRMA, \
    InternalRMAState, DirectRefundRMA, TestRMA
from sales.models import Transaction, TransactionLine, SalesTransactionLine, \
    RefundTransactionLine, InvalidDataException, Payment
from stock.models import Stock
from stock.stocklabel import OrderLabel
from logistics.models import StockWish
from money.models import Price, Money


class BasicTests(TestCase, TestData):

    def setUp(self):
        self.setup_base_data()

    def test_simple_store_customer_rma_task(self):
        self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments()
        self.create_transactions_article_type()
        trans = Transaction.objects.all().first()
        crt = CustomerRMATask(customer=self.customer_person_1, receipt=trans)
        crt.save()
        self.assertFalse(crt.handled)

    def test_cause_abstraction(self):
        cause = RMACause()
        with self.assertRaises(AbstractionError):
            cause.save()

    def test_stock_rma(self):
        StockWish.create_stock_wish(user_modified=self.user_1, articles_ordered=[(self.articletype_1, 5),(self.articletype_2, 5)])
        self.create_suporders(article_1=5, article_2=5)
        self.create_packingdocuments()
        value = Stock.objects.get(article=self.articletype_1).book_value
        srma = StockRMA(article_type=self.articletype_1, user_modified=self.user_1, value= value)
        srma.save()
        irs = InternalRMA.objects.all()
        self.assertEqual(len(irs), 1)
        self.assertEqual(irs[0].rma_cause.stockrma, srma)
        self.assertEqual(irs[0].customer, None)
        self.assertEqual(irs[0].state, 'B')
        irls = InternalRMAState.objects.get()
        self.assertEqual(irls.state, 'B')
        self.assertEqual(irls.internal_rma, irs[0])

    def test_refund_illegal_options(self):
        self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments()
        self.create_transactions_article_type()
        stl = SalesTransactionLine.objects.first()
        rcpt = Transaction.objects.first()
        crt = CustomerRMATask(customer=self.customer_person_1, receipt=rcpt)
        crt.save()
        tra = TestRMA(user_modified=self.user_1, transaction_line=stl, state='U', customer_rma_task=crt)
        tra.save()
        rfl = RefundTransactionLine(user_modified=self.user_1, count=-1, test_rma=tra, creates_rma=True)
        with self.assertRaises(InvalidDataException):
            rfl.save()

    def test_direct_refund_rma(self):
        # Test creation of RMA. No customer RMA was generated
        self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments()
        self.create_transactions_article_type()
        stl = SalesTransactionLine.objects.first()
        price = stl.price # type: Price
        rfl = RefundTransactionLine(user_modified=self.user_1, count=-1, sold_transaction_line= stl,
                                    creates_rma=True, price=price)
        money = Money(amount=price.amount*-1, currency=self.currency_eur)
        pymnt = Payment(amount=money, payment_type=self.paymenttype_maestro)
        Transaction.create_transaction(user=self.user_1, payments=[pymnt], transaction_lines=[rfl])
        drm = DirectRefundRMA.objects.get()
        irma = InternalRMA.objects.get()
        self.assertEqual(drm.refund_line, rfl)
        self.assertEqual(irma.customer, None)
        self.assertEqual(irma.rma_cause.directrefundrma, drm)
        self.assertEqual(irma.state, 'B')
        self.assertEqual(irma.description, '')





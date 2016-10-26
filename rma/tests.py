from django.test import TestCase
from tools.testing import TestData
from rma.models import CustomerRMATask, RMACause, AbstractionError, StockRMA, InternalRMA, \
    InternalRMAState, DirectRefundRMA, TestRMA, CustomerTaskDescription, RMACountError
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

    def test_customer_rma_task_comments(self):
        self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments()
        self.create_transactions_article_type()
        trans = Transaction.objects.first()
        crt = CustomerRMATask(customer=self.customer_person_1, receipt=trans)
        crt.save()
        c1 = CustomerTaskDescription(customer_rma_task=crt, text="Something broke I think.", user_modified=self.user_1)
        c1.save()
        c2 = CustomerTaskDescription(customer_rma_task=crt, text="It did break.", user_modified= self.user_2)
        c2.save()
        comments = CustomerTaskDescription.objects.filter(customer_rma_task=crt)
        self.assertEqual(len(comments), 2)

    def test_testrma_in_customer_rma_task(self):
        self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments()
        self.create_transactions_article_type()
        trans = Transaction.objects.first()
        stl = SalesTransactionLine.objects.filter(transaction=trans).first()
        crt = CustomerRMATask(customer=self.customer_person_1, receipt=trans)
        crt.save()
        tra = TestRMA(user_modified=self.user_1, transaction_line=stl, customer_rma_task=crt)
        tra.save()
        self.assertEqual(tra.state, 'U')
        ira = InternalRMA.objects.get()
        self.assertEqual(ira.rma_cause.testrma, tra)
        self.assertEqual(ira.customer.id, self.customer_person_1.id)
        self.assertEqual(ira.state, 'B')

    def test_testrma_overloading_number_of_testrmas(self):
        self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments()
        self.create_transactions_article_type(article_1=2)
        trans = Transaction.objects.first()
        stl = SalesTransactionLine.objects.filter(transaction=trans, article=self.articletype_1).first()
        crt = CustomerRMATask(customer=self.customer_person_1, receipt=trans)
        crt.save()
        tra1 = TestRMA(user_modified=self.user_1, transaction_line=stl, customer_rma_task=crt)
        tra1.save()
        tra2 = TestRMA(user_modified=self.user_1, transaction_line=stl, customer_rma_task=crt)
        tra2.save()
        with self.assertRaises(RMACountError):
            tra3 = TestRMA(user_modified=self.user_1, transaction_line=stl, customer_rma_task=crt)
            tra3.save()

    def test_testrma_correct_closing_states(self):
        self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments()
        self.create_transactions_article_type(article_1=2)
        trans = Transaction.objects.first()
        stl = SalesTransactionLine.objects.filter(transaction=trans, article=self.articletype_1).first()
        crt = CustomerRMATask(customer=self.customer_person_1, receipt=trans)
        crt.save()
        tra1 = TestRMA(user_modified=self.user_1, transaction_line=stl, customer_rma_task=crt)
        tra1.save()
        tra2 = TestRMA(user_modified=self.user_1, transaction_line=stl, customer_rma_task=crt)
        tra2.save()
        tra2.transition('F', self.user_1)
        tra3 = TestRMA(user_modified=self.user_1, transaction_line=stl, customer_rma_task=crt)
        tra3.save()

    def test_counted_customer_rmas(self):
        self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments()
        self.create_transactions_article_type()
        trans = Transaction.objects.first()
        crt = CustomerRMATask(customer=self.customer_person_1, receipt=trans)
        crt.save()
        self.assertEquals(crt.has_open_rmas_for_customer(), False)
        stl = SalesTransactionLine.objects.filter(transaction=trans, article=self.articletype_1).first()
        tra1 = TestRMA(user_modified=self.user_1, transaction_line=stl, customer_rma_task=crt)
        tra1.save()
        self.assertEquals(crt.has_open_rmas_for_customer(), True)
        self.assertEquals(len(crt.get_open_customer_rmas()), 1)
        tra2 = TestRMA(user_modified=self.user_1, transaction_line=stl, customer_rma_task=crt)
        tra2.save()
        self.assertEquals(crt.has_open_rmas_for_customer(), True)
        self.assertEquals(len(crt.get_open_customer_rmas()), 2)
        tra2.transition('F', self.user_1)
        self.assertEquals(crt.has_open_rmas_for_customer(), True)
        self.assertEquals(len(crt.get_open_customer_rmas()), 1)
        tra1.transition('F', self.user_2)
        self.assertEquals(crt.has_open_rmas_for_customer(), False)
        self.assertEquals(len(crt.get_open_customer_rmas()), 0)
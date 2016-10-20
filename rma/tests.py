from django.test import TestCase
from tools.testing import TestData
from rma.models import CustomerRMATask, RMACause, AbstractionError, StockRMA
from sales.models import Transaction
from stock.models import Stock
from stock.stocklabel import OrderLabel
from logistics.models import StockWish


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

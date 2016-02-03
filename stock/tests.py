from decimal import Decimal

# Create your tests here.
from datetime import time, datetime
from django.test import TestCase

from stock.models import Stock, StockModification, StockLog
from article.models import ArticleType
from money.models import Currency, VAT, SalesPrice


class StockTest(TestCase):
    def setup(self):
        pass

    def testAddStockDirectly(self):
        i = 0
        try:
            sp = SalesPrice(amount=Decimal("2.00000"),currency=Currency("USD"), vat=Decimal("1.21"),cost=Decimal("2.19000"))
            art = ArticleType()
            art.save()
            Stock.objects.create(article=art,salesprice=sp,count=2)
        except AssertionError:
            i = 1
        self.assertEquals(i,1)

    def testAddToStock(self):
        sp = SalesPrice(amount=Decimal("2.00000"),currency=Currency("USD"), vat=Decimal("1.21"),cost=Decimal("2.19000"))
        art = ArticleType()
        art.save()
        ES = StockModification(article=art,salesprice=sp,count=2)
        sl = StockLog.log("henk",[ES])


    def testAddMultipleToStock(self):
        sp = SalesPrice(amount=Decimal("2.00000"),currency=Currency("USD"), vat=Decimal("1.21"),cost=Decimal("2.19000"))
        art = ArticleType()
        art.save()
        ES = StockModification(article=art,salesprice=sp,count=2)
        ES2 = StockModification(article=art,salesprice=sp,count=2)
        sl = StockLog.log("henk",[ES, ES2])

    def testAddTwoDifferentArticlesToStock(self):
        sp = SalesPrice(amount=Decimal("2.00000"),currency=Currency("USD"), vat=Decimal("1.21"),cost=Decimal("2.19000"))
        art = ArticleType()
        art.save()
        art2 = ArticleType()
        art2.save()
        ES = StockModification(article=art,salesprice=sp,count=2)
        ES2 = StockModification(article=art2,salesprice=sp,count=2)
        sl = StockLog.log("henk",[ES, ES2])



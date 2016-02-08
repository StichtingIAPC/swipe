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
            sp = SalesPrice(amount=Decimal("2.00000"), currency=Currency("USD"), vat=Decimal("1.21"),
                            cost=Decimal("2.19000"))
            art = ArticleType(name="P1")
            art.save()
            Stock.objects.create(article=art, salesprice=sp, count=2)
        except AssertionError:
            i = 1
        self.assertEquals(i, 1)

    def testAddToStock(self):
        sp = SalesPrice(amount=Decimal("2.00000"), currency=Currency("USD"), vat=Decimal("1.21"),
                        cost=Decimal("2.19000"))
        art = ArticleType(name="P1")
        art.save()
        ES = StockModification(article=art, salesprice=sp, count=2)
        sl = StockLog.log("henk", [ES])
        print("Start single")

        stocks = Stock.objects.all()
        for stock in stocks:
            print(stock.article == art)
            print(stock.count)

    def testAddMultipleToStock(self):
        sp = SalesPrice(amount=Decimal("2.00000"), currency=Currency("USD"), vat=Decimal("1.21"),
                        cost=Decimal("2.19000"))
        art = ArticleType(name="P1")
        art.save()
        ES = StockModification(article=art, salesprice=sp, count=2)
        ES2 = StockModification(article=art, salesprice=sp, count=3)
        sl = StockLog.log("henk", [ES, ES2])
        stocks = Stock.objects.all()
        print("Start multiple to stock")
        for stock in stocks:
            print(stock.article == art)
            print(stock.count)

    def testAddTwoDifferentArticlesToStock(self):
        sp = SalesPrice(amount=Decimal("2.00000"), currency=Currency("USD"), vat=Decimal("1.21"),
                        cost=Decimal("2.19000"))
        art = ArticleType(name="P1")
        art.save()
        art2 = ArticleType(name="P2")
        art2.save()
        ES = StockModification(article=art, salesprice=sp, count=2)
        ES2 = StockModification(article=art2, salesprice=sp, count=3)
        stocks = Stock.objects.all()
        print("Start two different")
        sl = StockLog.log("henk", [ES, ES2])
        for stock in stocks:
            print(stock.article == art)
            print(stock.count)

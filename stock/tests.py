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
        vat = VAT(vatrate=Decimal("1.21"), name="HIGH", active=True)
        vat.save()
        try:
            sp = SalesPrice(amount=Decimal("2.00000"), currency=Currency("USD"), vat=Decimal("1.21"),
                            cost=Decimal("2.19000"))
            art = ArticleType(name="P1",vat=vat)
            art.save()
            Stock.objects.create(article=art, salesprice=sp, count=2)
        except AssertionError:
            i = 1
        self.assertEquals(i, 1)

    def testAddToStock(self):
        vat = VAT(vatrate=Decimal("1.21"),name="HIGH",active=True)
        vat.save()
        sp = SalesPrice(amount=Decimal("2.00000"), currency=Currency("USD"), vat=Decimal("1.21"),
                        cost=Decimal("2.19000"))

        art = ArticleType(name="P1",vat=vat)
        art.save()
        ES = StockModification(article=art, salesprice=sp, count=2)
        ES2 = StockModification(article=art, salesprice=sp, count=2)

        StockLog.log("henk", [ES])
        StockLog.log("henk", [ES])
        print("end log)")
        stocks = Stock.objects.all()
        for stock in stocks:
            print(stock)
            self.assertEquals(stock.article, art)

            self.assertEquals(stock.salesprice.amount, Decimal("2.87514"))
            self.assertEquals(stock.salesprice.cost,sp.cost)

    def testAddMultipleToStock(self):
        vat = VAT(vatrate=Decimal("1.21"),name="HIGH",active=True)
        vat.save()
        sp = SalesPrice(amount=Decimal("2.00000"), currency=Currency("USD"), vat=Decimal("1.21"),
                        cost=Decimal("1.00000"))
        sp2 = SalesPrice(amount=Decimal("2.00000"), currency=Currency("USD"), vat=Decimal("1.21"),
                        cost=Decimal("10.00000"))
        art = ArticleType(name="P1", vat=vat)
        art.save()
        ES = StockModification(article=art, salesprice=sp, count=5)
        ES2 = StockModification(article=art, salesprice=sp2, count=1)
        sl = StockLog.log("henk", [ES, ES2])
        stocks = Stock.objects.all()
        for stock in stocks:
            self.assertEqual(stock.count,6)
            self.assertEquals(stock.article, art)
            self.assertEquals(stock.salesprice,SalesPrice(amount=Decimal("3.28212"),currency=Currency("USD"),vat=Decimal("1.21"),cost=Decimal("2.50")))

    def testAddTwoDifferentArticlesToStock(self):
        vat = VAT(vatrate=Decimal("1.21"),name="HIGH",active=True)
        vat.save()
        sp = SalesPrice(amount=Decimal("2.00000"), currency=Currency("USD"), vat=Decimal("1.21"),
                        cost=Decimal("2.19000"))
        art = ArticleType(name="P1",vat=vat)
        art.save()
        art2 = ArticleType(name="P2",vat=vat)
        art2.save()
        ES = StockModification(article=art, salesprice=sp, count=2)
        ES2 = StockModification(article=art2, salesprice=sp, count=3)
        stocks = Stock.objects.all()
        sl = StockLog.log("henk", [ES, ES2])
        for stock in stocks:
            if stock.article == art:
                self.assertEqual(stock.count,ES.count)
            if stock.article == art2:
                self.assertEqual(stock.count,ES2.count)


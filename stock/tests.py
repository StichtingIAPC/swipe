from decimal import Decimal

# Create your tests here.
from datetime import time, datetime
from django.test import TestCase

from stock.models import Stock, StockModification, StockLog
from article.models import ArticleType
from money.models import Currency, VAT, SalesPrice, Cost


class StockTest(TestCase):
    def setup(self):
        pass

    def testAddStockDirectly(self):
        cur = Currency("EUR")

        i = 0
        vat = VAT(vatrate=Decimal("1.21"), name="HIGH", active=True)
        vat.save()
        try:
            sp = Cost(amount=Decimal("1.00000"),currency=cur)
            art = ArticleType(name="P1", vat=vat)
            art.save()
            Stock.objects.create(article=art, cost=sp, count=2)
        except AssertionError:
            i = 1
        self.assertEquals(i, 1)

    def testAddToStock(self):
        cur = Currency("EUR")

        vat = VAT(vatrate=Decimal("1.21"), name="HIGH", active=True)
        vat.save()
        sp = Cost(amount=Decimal("2.00000"),currency=cur)

        art = ArticleType(name="P1", vat=vat)
        art.save()
        ES = StockModification(article=art, cost=sp, count=2, is_in=True)
        ES2 = StockModification(article=art, cost=sp, count=2, is_in=True)

        StockLog.log("henk", [ES])
        StockLog.log("henk", [ES])
        stocks = Stock.objects.all()
        for stock in stocks:
            self.assertEquals(stock.article, art)
            self.assertEquals(stock.cost.amount,  sp.amount)

    def testAddMultipleToStock(self):
        cur = Currency("EUR")

        vat = VAT(vatrate=Decimal("1.21"), name="HIGH", active=True)
        vat.save()
        sp = Cost(amount=Decimal("1.00000"),currency=cur)
        sp2 = Cost(amount=Decimal("1.00000"),currency=cur)
        art = ArticleType(name="P1", vat=vat)
        art.save()
        ES = StockModification(article=art, cost=sp, count=5, is_in=True)
        ES2 = StockModification(article=art, cost=sp2, count=1, is_in=True)
        sl = StockLog.log("henk", [ES, ES2])
        stocks = Stock.objects.all()
        for stock in stocks:
            self.assertEqual(stock.count, 6)
            self.assertEquals(stock.article, art)
            self.assertEquals(stock.cost.amount,Decimal("1.00000"))

    def testAddTwoDifferentArticlesToStock(self):
        cur = Currency("EUR")

        vat = VAT(vatrate=Decimal("1.21"), name="HIGH", active=True)
        vat.save()
        sp = Cost(amount=Decimal("1.00000"),currency=cur)
        art = ArticleType(name="P1", vat=vat)
        art.save()
        art2 = ArticleType(name="P2", vat=vat)
        art2.save()
        ES = StockModification(article=art, cost=sp, count=2, is_in=True)
        ES2 = StockModification(article=art2, cost=sp, count=3, is_in=True)
        stocks = Stock.objects.all()
        sl = StockLog.log("henk", [ES, ES2])
        for stock in stocks:
            if stock.article == art:
                self.assertEqual(stock.count, ES.count)
            if stock.article == art2:
                self.assertEqual(stock.count, ES2.count)

    def testTwoArticleMerges(self):
        vat = VAT(vatrate=Decimal("1.21"), name="HIGH", active=True)
        cur = Currency("EUR")
        vat.save()
        sp = Cost(amount=Decimal("1.00000"),currency=cur)
        sp2 = Cost(amount=Decimal("1.00000"),currency=cur)
        art = ArticleType(name="P1", vat=vat)
        art.save()
        art2 = ArticleType(name="P2", vat=vat)
        art2.save()
        ES = StockModification(article=art, cost=sp, count=2, is_in=True)
        ES2 = StockModification(article=art2, cost=sp2, count=3, is_in=True)
        StockLog.log("henk", [ES, ES2])
        StockLog.log("henk", [ES, ES2])
        StockLog.log("henk", [ES, ES2, ES])
        ES2 = StockModification(article=art2, cost=sp2, count=1, is_in=False)
        StockLog.log("henk", [ES2])

        st1 = Stock.objects.get(article=art)
        self.assertEqual(st1.count, 8)
        st2 = Stock.objects.get(article=art2)
        self.assertEqual(st1.cost.currency, cur)
        self.assertEqual(st1.cost.amount, Decimal("1.00000"))
        self.assertEqual(st2.count, 8)
        self.assertEqual(st2.cost.currency, cur)
        self.assertEqual(st2.cost.amount, Decimal("1.00000"))

    def testOneTwoThreeFourFiveSix(self):
        cur = Currency("EUR")

        vat = VAT(vatrate=Decimal("1.21"), name="HIGH", active=True)
        vat.save()

        art = ArticleType(name="P1", vat=vat)
        art.save()
        for i in range(1, 7):  # 1 to 6. Average: should be 3.5
            cost=Cost(amount=Decimal(str(i)), currency=cur)
            es = StockModification(article=art, cost=cost, count=1, is_in=True)
            StockLog.log("LOG" + str(i), [es])

        st = Stock.objects.get(article=art)
        self.assertEqual(st.cost.currency, cur)
        # Test is average equals 3.5
        self.assertEqual(st.cost.amount, Decimal("3.50000"))

    def testMinusOneTwoThreeFourFiveSix(self):
        cur = Currency("EUR")

        vat = VAT(vatrate=Decimal("1.21"), name="HIGH", active=True)
        vat.save()

        art = ArticleType(name="P1", vat=vat)
        art.save()
        i=0
        try:
            for i in range(1, 7):  # 1 to 6. Average: should be 3.5
                sp = Cost(amount=Decimal(str(i)),currency=cur)
                print(i)
                es = StockModification(article=art, cost=sp, count=1, is_in=False)
                StockLog.log("LOG" + str(i), [es])
        except Exception:
            print(i)
            pass
        self.assertEqual(i,1)

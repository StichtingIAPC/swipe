from decimal import Decimal

# Create your tests here.
from datetime import time, datetime
from django.test import TestCase

from stock.models import Stock, StockModification, StockLog
from article.models import ArticleType
from money.models import Currency, VAT, Cost


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
            Stock.objects.create(article=art, book_value=sp, count=2)
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
        ES = StockModification(article=art, book_value=sp, count=2, is_in=True)
        ES2 = StockModification(article=art, book_value=sp, count=2, is_in=True)

        StockLog.log("henk", [ES])
        StockLog.log("henk", [ES])
        stocks = Stock.objects.all()
        for stock in stocks:
            self.assertEquals(stock.article, art)
            self.assertEquals(stock.book_value.amount,  sp.amount)

    def testAddMultipleToStock(self):
        cur = Currency("EUR")

        vat = VAT(vatrate=Decimal("1.21"), name="HIGH", active=True)
        vat.save()
        sp = Cost(amount=Decimal("1.00000"),currency=cur)
        sp2 = Cost(amount=Decimal("1.00000"),currency=cur)
        art = ArticleType(name="P1", vat=vat)
        art.save()
        ES = StockModification(article=art, book_value=sp, count=5, is_in=True)
        ES2 = StockModification(article=art, book_value=sp2, count=1, is_in=True)
        sl = StockLog.log("henk", [ES, ES2])
        stocks = Stock.objects.all()
        for stock in stocks:
            self.assertEqual(stock.count, 6)
            self.assertEquals(stock.article, art)
            self.assertEquals(stock.book_value.amount,Decimal("1.00000"))

    def testAddTwoDifferentArticlesToStock(self):
        cur = Currency("EUR")

        vat = VAT(vatrate=Decimal("1.21"), name="HIGH", active=True)
        vat.save()
        sp = Cost(amount=Decimal("1.00000"),currency=cur)
        art = ArticleType(name="P1", vat=vat)
        art.save()
        art2 = ArticleType(name="P2", vat=vat)
        art2.save()
        ES = StockModification(article=art, book_value=sp, count=2, is_in=True)
        ES2 = StockModification(article=art2, book_value=sp, count=3, is_in=True)
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
        ES = StockModification(article=art, book_value=sp, count=2, is_in=True)
        ES2 = StockModification(article=art2, book_value=sp2, count=3, is_in=True)
        StockLog.log("henk", [ES, ES2])
        StockLog.log("henk", [ES, ES2])
        StockLog.log("henk", [ES, ES2, ES])
        ES2 = StockModification(article=art2, book_value=sp2, count=1, is_in=False)
        StockLog.log("henk", [ES2])

        st1 = Stock.objects.get(article=art)
        self.assertEqual(st1.count, 8)
        st2 = Stock.objects.get(article=art2)
        self.assertEqual(st1.book_value.currency, cur)
        self.assertEqual(st1.book_value.amount, Decimal("1.00000"))
        self.assertEqual(st2.count, 8)
        self.assertEqual(st2.book_value.currency, cur)
        self.assertEqual(st2.book_value.amount, Decimal("1.00000"))

    def testOneTwoThreeFourFiveSix(self):
        cur = Currency("EUR")

        vat = VAT(vatrate=Decimal("1.21"), name="HIGH", active=True)
        vat.save()

        art = ArticleType(name="P1", vat=vat)
        art.save()
        for i in range(1, 7):  # 1 to 6. Average: should be 3.5
            book_value = Cost(amount=Decimal(str(i)), currency=cur)
            es = StockModification(article=art, book_value=book_value, count=1, is_in=True)
            StockLog.log("LOG" + str(i), [es])

        st = Stock.objects.get(article=art)
        self.assertEqual(st.book_value.currency, cur)
        # Test is average equals 3.5
        self.assertEqual(st.book_value.amount, Decimal("3.50000"))

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
                es = StockModification(article=art, book_value=sp, count=1, is_in=False)
                StockLog.log("LOG" + str(i), [es])
        except Exception:
            pass
        self.assertEqual(i,1)

    def testDifferentCurrencies(self):
        eur = Currency("EUR")

        vat = VAT(vatrate=Decimal("1.21"), name="HIGH", active=True)
        vat.save()

        art = ArticleType(name="P1", vat=vat)
        art.save()

        sp = Cost(amount=Decimal(str(1)),currency=eur)
        es = StockModification(article=art, book_value=sp, count=1, is_in=True)
        StockLog.log("LOG", [es])

        usd = Currency("USD")
        sp = Cost(amount=Decimal(str(1)),currency=usd)
        es = StockModification(article=art, book_value=sp, count=1, is_in=True)

          # 1 to 6. Average: should be 3.5
        i=0
        try:
            StockLog.log("LOG", [es])
        except Exception:
            i=1
        self.assertEqual(i,1)

        #Interesting test: there should be no additional lines in Stocklog and Stockmodification
        self.assertEqual(len(StockLog.objects.all()),1)
        self.assertEqual(len(StockModification.objects.all()),1)

        sp = Cost(amount=Decimal(str(1)),currency=eur)
        es = StockModification(article=art, book_value=sp, count=1, is_in=True)
        i=0
        try:
            StockLog.log("LOG", [es])
        except Exception:
            i=1
        self.assertEqual(i,0)
        self.assertEqual(len(StockLog.objects.all()),2)
        self.assertEqual(len(StockModification.objects.all()),2)



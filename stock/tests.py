from decimal import Decimal

# Create your tests here.
from datetime import time, datetime
from django.test import TestCase

from money.exceptions import CurrencyInconsistencyError
from stock.exceptions import Id10TError, StockSmallerThanZeroError
from stock.models import Stock, StockModification, StockLog
from article.models import ArticleType
from money.models import Currency, VAT, Cost


class StockTest(TestCase):
    def setup(self):
        pass

    def testAddStockDirectly(self):
        """
        Test that tries to add an item to the stock directly.
        """

        i = 0
        cur = Currency("EUR")
        vat = VAT.objects.create(vatrate=Decimal("1.21"), name="HIGH", active=True)

        try:
            sp = Cost(amount=Decimal("1.00000"), currency=cur)
            art = ArticleType.objects.create(name="P1", vat=vat)
            Stock.objects.create(article=art, book_value=sp, count=2)

        except Id10TError:
            i = 1

        self.assertEquals(i, 1)

    def testAddToStock(self):
        """
        Test that tries to add 2 of the same articles to the stock properly.
        """

        # Create some objects to use in the tests
        cur = Currency("EUR")
        vat = VAT.objects.create(vatrate=Decimal("1.21"), name="HIGH", active=True)
        art = ArticleType.objects.create(name="Product1", vat=vat)
        sp = Cost(amount=Decimal("2.00000"), currency=cur)

        # Construct entry list for StockLog
        entries = [{
            'article': art,
            'book_value': sp,
            'count': 2,
            'is_in': True
        }]

        # Execute two stock modifications, creating two StockLogs
        log_1 = StockLog.construct(description="AddToStockTest1", entries=entries)
        log_2 = StockLog.construct(description="AddToStockTest2", entries=entries)  # Re-using entries for test.

        # Check that we only added one type of article to the stock
        self.assertEquals(len(Stock.objects.all()), 1)

        # Check if number of items in StockLog is correct
        self.assertEquals(len(log_1.stockmodification_set.all()), 1)
        self.assertEquals(len(log_2.stockmodification_set.all()), 1)

        # Check if StockModification instance in log 1 is different from item in log 2
        self.assertNotEquals(log_1.stockmodification_set.all()[0], log_2.stockmodification_set.all()[0])

        # Get stock for article
        art_stock = Stock.objects.get(article=art)

        # Check if the article in stock is the article we specified
        self.assertEquals(art_stock.article, art)

        # Check if the number of items in stock is correct
        self.assertEquals(art_stock.count, 4)

        # Check if the book value of the item is equal to the cost of the article
        self.assertEquals(art_stock.book_value.amount,  sp.amount)

    def testAddMultipleToStock(self):
        """
        Test that tries to add 5 and 1 of an article to the stock in separate entries.
        """

        # Create some objects to use in the tests
        cur = Currency("EUR")
        vat = VAT.objects.create(vatrate=Decimal("1.21"), name="HIGH", active=True)
        sp = Cost(amount=Decimal("1.00000"), currency=cur)
        sp2 = Cost(amount=Decimal("1.00000"), currency=cur)
        art = ArticleType.objects.create(name="P1", vat=vat)

        # Construct entry list for StockLog
        entries = [{
            'article': art,
            'book_value': sp,
            'count': 5,
            'is_in': True
        }, {
            'article': art,
            'book_value': sp2,
            'count': 1,
            'is_in': True
        }]

        # Execute the stock modification, creating a StockLog
        log_1 = StockLog.construct(description="MultipleProductsTest", entries=entries)

        # Check that we only added one type of article to the stock
        self.assertEquals(len(Stock.objects.all()), 1)

        # Check if number of items in the StockLog is correct
        self.assertEquals(len(log_1.stockmodification_set.all()), 2)

        # Check if StockModification instances in the log are different from each other
        self.assertNotEquals(log_1.stockmodification_set.all()[0], log_1.stockmodification_set.all()[1])

        # Get stock for article
        art_stock = Stock.objects.get(article=art)

        # Check if the article in stock is the article we specified
        self.assertEquals(art_stock.article, art)

        # Check if the number of items in stock is correct
        self.assertEquals(art_stock.count, 6)

        # Check if the book value of the item is equal to the cost of the article
        self.assertEquals(art_stock.book_value.amount, Decimal("1.00000"))

    def testAddTwoDifferentArticlesToStock(self):
        """
        Test that adds two different articles to the stock.
        """

        # Create some objects to use in the tests
        cur = Currency("EUR")
        vat = VAT.objects.create(vatrate=Decimal("1.21"), name="HIGH", active=True)
        sp = Cost(amount=Decimal("1.00000"), currency=cur)
        art = ArticleType.objects.create(name="Product1", vat=vat)
        art2 = ArticleType.objects.create(name="Product2", vat=vat)

        # Construct entry list for StockLog
        entries = [{
            'article': art,
            'book_value': sp,
            'count': 2,
            'is_in': True
        }, {
            'article': art2,
            'book_value': sp,
            'count': 3,
            'is_in': True
        }]

        # Execute the stock modification, creating a StockLog
        log_1 = StockLog.construct(description="MultipleArticlesTest", entries=entries)

        # Check that we added two types of article to the stock
        self.assertEquals(len(Stock.objects.all()), 2)

        # Check if number of items in the StockLog is correct
        self.assertEquals(len(log_1.stockmodification_set.all()), 2)

        # Check if StockModification instances in the log are different from each other
        self.assertNotEquals(log_1.stockmodification_set.all()[0], log_1.stockmodification_set.all()[1])

        # Get stock for the two articles
        art_stock = Stock.objects.get(article=art)
        art2_stock = Stock.objects.get(article=art2)

        # Check if the number of items per article are correct
        self.assertEquals(art_stock.count, 2)
        self.assertEquals(art2_stock.count, 3)

        # Check if the book value of the items are equal to the cost of the articles
        self.assertEquals(art_stock.book_value.amount, sp.amount)
        self.assertEquals(art2_stock.book_value.amount, sp.amount)

    def testTwoArticleMerges(self):
        """
        Test that adds two types of articles, then sells one of them.
        """

        # Create some objects to use in the tests
        cur = Currency("EUR")
        vat = VAT.objects.create(vatrate=Decimal("1.21"), name="HIGH", active=True)
        sp = Cost(amount=Decimal("1.00000"), currency=cur)
        sp2 = Cost(amount=Decimal("1.00000"), currency=cur)
        art = ArticleType.objects.create(name="Product1", vat=vat)
        art2 = ArticleType.objects.create(name="Product2", vat=vat)

        # Construct some entries to use
        entry_1 = {  # 2 of Product1 in
            'article': art,
            'book_value': sp,
            'count': 2,
            'is_in': True
        }
        entry_2 = {  # 3 of Product2 in
            'article': art2,
            'book_value': sp2,
            'count': 3,
            'is_in': True
        }
        entry_3 = {  # 1 of Product2 out
            'article': art2,
            'book_value': sp2,
            'count': 1,
            'is_in': False
        }

        # Execute the needed modifications
        log_1 = StockLog.construct(description="Get 2xProduct1 3xProduct2", entries=[entry_1, entry_2])
        log_2 = StockLog.construct(description="Get 2xProduct1 3xProduct2", entries=[entry_1, entry_2])
        log_3 = StockLog.construct(description="Get 2xProduct1 3xProduct2 2xProduct1",
                                   entries=[entry_1, entry_2, entry_1])
        log_4 = StockLog.construct(description="Sell 1xProduct2", entries=[entry_3])

        # Get resulting stocks
        art_stock = Stock.objects.get(article=art)
        art2_stock = Stock.objects.get(article=art2)

        # Check number of StockModifications in StockLogs
        self.assertEqual(len(log_1.stockmodification_set.all()), 2)
        self.assertEqual(len(log_2.stockmodification_set.all()), 2)
        self.assertEqual(len(log_3.stockmodification_set.all()), 3)
        self.assertEqual(len(log_4.stockmodification_set.all()), 1)

        # Check if number of items in stock is correct
        self.assertEqual(art_stock.count, 8)
        self.assertEqual(art2_stock.count, 8)

        # Check if book value of stock is correct
        self.assertEqual(art_stock.book_value.amount, Decimal("1.00000"))
        self.assertEqual(art2_stock.book_value.amount, Decimal("1.00000"))

        # Check if currency of stock is correct
        self.assertEqual(art_stock.book_value.currency, cur)
        self.assertEqual(art2_stock.book_value.currency, cur)

    def testOneTwoThreeFourFiveSix(self):
        """
        Test that adds 6 articles with increasing book value, and checks if the resulting book value is correct.
        """

        # Create some objects to use in the tests
        cur = Currency("EUR")
        vat = VAT.objects.create(vatrate=Decimal("1.21"), name="HIGH", active=True)
        art = ArticleType.objects.create(name="Product1", vat=vat)

        for i in range(1, 7):  # 1 to 6. Average should be 3.5
            # Define book value
            book_value = Cost(amount=Decimal(str(i)), currency=cur)

            # Construct entry for StockLog
            entries = [{
                'article': art,
                'book_value': book_value,
                'count': 1,
                'is_in': True
            }]

            # Do stock modification
            StockLog.construct(description="AverageTest{}".format(i), entries=entries)

        # Get stock for article
        st = Stock.objects.get(article=art)

        # Check if the currency of the book value is correct
        self.assertEqual(st.book_value.currency, cur)

        # Check if the average equals 3.5
        self.assertEqual(st.book_value.amount, Decimal("3.50000"))

    def testMinusOneTwoThreeFourFiveSix(self):
        """
        Test that tries to sell 6 items with increasing book value from an empty stock.
        """
        # Create some objects to use in the tests
        i = 0
        cur = Currency("EUR")
        vat = VAT.objects.create(vatrate=Decimal("1.21"), name="HIGH", active=True)
        art = ArticleType.objects.create(name="Product1", vat=vat)

        try:
            for i in range(1, 7):  # 1 to 6. Average should be 3.5
                # Define book value
                book_value = Cost(amount=Decimal(str(i)), currency=cur)

                # Construct entry for StockLog
                entries = [{
                    'article': art,
                    'book_value': book_value,
                    'count': 1,
                    'is_in': False
                }]

                # Do stock modification
                StockLog.construct(description="NegativeStockTest{}".format(i), entries=entries)

        except StockSmallerThanZeroError:
            i = 1

        self.assertEqual(i,1)

    def testDifferentCurrencies(self):
        """
        Test that
        """

        # Create some objects to use in the tests
        i = 0
        eur = Currency("EUR")
        usd = Currency("USD")
        vat = VAT.objects.create(vatrate=Decimal("1.21"), name="HIGH", active=True)
        cost_eur = Cost(amount=Decimal(str(1)), currency=eur)  # 1 euro
        cost_usd = Cost(amount=Decimal(str(1)), currency=usd)  # 1 dollar
        art = ArticleType.objects.create(name="P1", vat=vat)

        # Add 1 article with cost 1 euro
        entries = [{
            'article': art,
            'book_value': cost_eur,
            'count': 1,
            'is_in': True
        }]
        StockLog.construct(description="AddEuroStock", entries=entries)

        # Check if the product was successfully added to the stock
        self.assertEqual(len(Stock.objects.all()), 1)
        self.assertEqual(len(StockLog.objects.all()), 1)
        self.assertEqual(len(StockModification.objects.all()), 1)

        # (Try to) add 1 article with cost 1 dollar
        entries = [{
            'article': art,
            'book_value': cost_usd,
            'count': 1,
            'is_in': True
        }]
        try:
            StockLog.construct(description="AddDollarStock", entries=entries)
        except CurrencyInconsistencyError:
            i = 1

        # Check if the CurrencyInconsistencyError occurred
        self.assertEqual(i, 1)

        # Check if there are no additional lines in the StockLog and StockModifications
        # The error should have rolled back the changes the second modification might have made
        self.assertEqual(len(StockLog.objects.all()), 1)
        self.assertEqual(len(StockModification.objects.all()), 1)

        # Try to add another item with a price of 1 euro
        entries = [{
            'article': art,
            'book_value': cost_eur,
            'count': 1,
            'is_in': True
        }]

        i = 0

        try:
            StockLog.construct(description="AddSecondEuroStock", entries=entries)
        except CurrencyInconsistencyError:
            i = 1

        # This should have worked, so i should still be 0
        self.assertEqual(i, 0)

        # Check if the stock has indeed changed
        self.assertEqual(len(StockLog.objects.all()),2)
        self.assertEqual(len(StockModification.objects.all()),2)

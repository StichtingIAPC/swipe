from decimal import Decimal

# Create your tests here.
import time
from django.test import TestCase
from unittest import skip
from money.exceptions import CurrencyInconsistencyError
from stock.exceptions import Id10TError, StockSmallerThanZeroError
from stock.stocklabel import *
from stock.models import Stock, StockChange, StockChangeSet
from article.models import ArticleType
from money.models import Currency, VAT, Cost
from swipe import settings
from swipe.settings import DELETE_STOCK_ZERO_LINES
from tools.management.commands.consistencycheck import Command


class StockTest(TestCase):
    def setup(self):
        pass

    def tearDown(self):
        self.assertEqual(Stock.do_check(),[])

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

    def testAddStockChangeDirectly(self):
        """
        Test that tries to add an item to the stock directly.
        """

        i = 0
        cur = Currency("EUR")
        vat = VAT.objects.create(vatrate=Decimal("1.21"), name="HIGH", active=True)

        try:
            sp = Cost(amount=Decimal("1.00000"), currency=cur)
            art = ArticleType.objects.create(name="P1", vat=vat)
            StockChange.objects.create(article= art,book_value= sp,count= 2,is_in= True)

        except Id10TError:
            i = 1

        self.assertEquals(i, 1)

    def testAddStockChangeSetDirectly(self):
        """
        Test that tries to add an item to the stock directly.
        """

        i = 0
        cur = Currency("EUR")
        vat = VAT.objects.create(vatrate=Decimal("1.21"), name="HIGH", active=True)

        try:
            sp = Cost(amount=Decimal("1.00000"), currency=cur)
            art = ArticleType.objects.create(name="P1", vat=vat)
            StockChangeSet.objects.create(memo="A")

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

        # Construct entry list for StockChangeSet
        entries = [{
            'article': art,
            'book_value': sp,
            'count': 2,
            'is_in': True
        }]

        # Execute two stock modifications, creating two StockLogs
        log_1 = StockChangeSet.construct(description="AddToStockTest1", entries=entries, enum=1)
        log_2 = StockChangeSet.construct(description="AddToStockTest2", entries=entries, enum=1)  # Re-using entries for test.

        # Check that we only added one type of article to the stock
        self.assertEquals(len(Stock.objects.all()), 1)

        # Check if number of items in StockChangeSet is correct
        self.assertEquals(len(log_1. stockchange_set.all()), 1)
        self.assertEquals(len(log_2. stockchange_set.all()), 1)

        # Check if StockChange instance in log 1 is different from item in log 2
        self.assertNotEquals(log_1. stockchange_set.all()[0], log_2. stockchange_set.all()[0])

        # Get stock for article
        art_stock = Stock.objects.get(article=art)

        # Check if the article in stock is the article we specified
        self.assertEquals(art_stock.article, art)

        # Check if the number of items in stock is correct
        self.assertEquals(art_stock.count, 4)

        # Check if the book value of the item is equal to the cost of the article
        self.assertEquals(art_stock.book_value.amount,  sp.amount)

    def testFuckOverDBAndTestConsistencyChecker(self):
        """
        Test that tries to add 2 of the same articles to the stock properly.
        """

        # Create some objects to use in the tests
        cur = Currency("EUR")
        vat = VAT.objects.create(vatrate=Decimal("1.21"), name="HIGH", active=True)
        art = ArticleType.objects.create(name="Product1", vat=vat)
        sp = Cost(amount=Decimal("2.00000"), currency=cur)

        # Construct entry list for StockChangeSet
        entries = [{
            'article': art,
            'book_value': sp,
            'count': 2,
            'is_in': True
        }]

        # Execute two stock modifications, creating two StockLogs
        log_1 = StockChangeSet.construct(description="AddToStockTest1", entries=entries, enum=1)
        log_2 = StockChangeSet.construct(description="AddToStockTest2", entries=entries, enum=1)  # Re-using entries for test.

        # Check that we only added one type of article to the stock
        self.assertEquals(len(Stock.objects.all()), 1)

        # Check if number of items in StockChangeSet is correct
        self.assertEquals(len(log_1. stockchange_set.all()), 1)
        self.assertEquals(len(log_2. stockchange_set.all()), 1)

        # Check if StockChange instance in log 1 is different from item in log 2
        self.assertNotEquals(log_1. stockchange_set.all()[0], log_2. stockchange_set.all()[0])

        # Get stock for article
        art_stock = Stock.objects.get(article=art)

        # Check if the article in stock is the article we specified
        self.assertEquals(art_stock.article, art)

        # Check if the number of items in stock is correct
        self.assertEquals(art_stock.count, 4)

        # Check if the book value of the item is equal to the cost of the article
        self.assertEquals(art_stock.book_value.amount,  sp.amount)

        # Create stock inconsistency
        tt = Stock.objects.get(pk=1)
        tt.count = tt.count +1 # Fuck over everything
        tt.save(indirect = True) # Nail in the coffin
        print("")
        err = Stock.do_check()
        self.assertEqual(err.__len__(), 1 )
        self.assertEqual(err[0]["line"],'1_None_None')
        tt.count = tt.count -1 # Unfuck everything
        tt.save(indirect = True) # Save it again

    @skip("Really heavy test, comment this line if you want to run it")
    def testConsistencyCheckerPerformance(self):

        """
        Test that tries to add 2 of the same articles to the stock properly.
        """

        # Create some objects to use in the tests
        cur = Currency("EUR")
        vat = VAT.objects.create(vatrate=Decimal("1.21"), name="HIGH", active=True)
        art = ArticleType.objects.create(name="Product1", vat=vat)
        sp = Cost(amount=Decimal("2.00000"), currency=cur)

        # Construct entry list for StockChangeSet
        entries = [{
            'article': art,
            'book_value': sp,
            'count': 2,
            'is_in': True
        }]

        # Execute two stock modifications, creating two StockLogs
        start = time.clock()
        for i in range(1, 100000):
            log_1 = StockChangeSet.construct(description="AddToStockTest1", entries=entries, enum=1)
        print("Time elapsed during generation: {}".format(time.clock() - start))

        print("Generated")
        # Create stock inconsistency
        tt = Stock.objects.get(pk=1)
        tt.count = tt.count +1 # Fuck over everything
        tt.save(indirect = True) # Nail in the coffin]
        start = time.clock()
        err = Stock.do_check()
        print("Time elapsed during checks: {}".format(time.clock() - start))

        self.assertEqual(err.__len__(), 1 )
        self.assertEqual(err[0]["Line"],'1_None_None')

        tt.count = tt.count -1 # Unfuck everything
        tt.save(indirect = True) # Save it again

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

        # Construct entry list for StockChangeSet
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

        # Execute the stock modification, creating a StockChangeSet
        log_1 = StockChangeSet.construct(description="MultipleProductsTest", entries=entries, enum=1)

        # Check that we only added one type of article to the stock
        self.assertEquals(len(Stock.objects.all()), 1)

        # Check if number of items in the StockChangeSet is correct
        self.assertEquals(len(log_1. stockchange_set.all()), 2)

        # Check if StockChange instances in the log are different from each other
        self.assertNotEquals(log_1. stockchange_set.all()[0], log_1. stockchange_set.all()[1])

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

        # Construct entry list for StockChangeSet
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

        # Execute the stock modification, creating a StockChangeSet
        log_1 = StockChangeSet.construct(description="MultipleArticlesTest", entries=entries, enum=1)

        # Check that we added two types of article to the stock
        self.assertEquals(len(Stock.objects.all()), 2)

        # Check if number of items in the StockChangeSet is correct
        self.assertEquals(len(log_1. stockchange_set.all()), 2)

        # Check if StockChange instances in the log are different from each other
        self.assertNotEquals(log_1. stockchange_set.all()[0], log_1. stockchange_set.all()[1])

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
        log_1 = StockChangeSet.construct(description="Get 2xProduct1 3xProduct2", entries=[entry_1, entry_2], enum=1)
        log_2 = StockChangeSet.construct(description="Get 2xProduct1 3xProduct2", entries=[entry_1, entry_2], enum=1)
        log_3 = StockChangeSet.construct(description="Get 2xProduct1 3xProduct2 2xProduct1",
                                         entries=[entry_1, entry_2, entry_1], enum=1)
        log_4 = StockChangeSet.construct(description="Sell 1xProduct2", entries=[entry_3], enum=1)

        # Get resulting stocks
        art_stock = Stock.objects.get(article=art)
        art2_stock = Stock.objects.get(article=art2)

        # Check number of  stockchanges in StockLogs
        self.assertEqual(len(log_1. stockchange_set.all()), 2)
        self.assertEqual(len(log_2. stockchange_set.all()), 2)
        self.assertEqual(len(log_3. stockchange_set.all()), 3)
        self.assertEqual(len(log_4. stockchange_set.all()), 1)

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

            # Construct entry for StockChangeSet
            entries = [{
                'article': art,
                'book_value': book_value,
                'count': 1,
                'is_in': True
            }]

            # Do stock modification
            StockChangeSet.construct(description="AverageTest{}".format(i), entries=entries, enum=1)

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

                # Construct entry for StockChangeSet
                entries = [{
                    'article': art,
                    'book_value': book_value,
                    'count': 1,
                    'is_in': False
                }]

                # Do stock modification
                StockChangeSet.construct(description="NegativeStockTest{}".format(i), entries=entries, enum=1)

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
        StockChangeSet.construct(description="AddEuroStock", entries=entries, enum=1)

        # Check if the product was successfully added to the stock
        self.assertEqual(len(Stock.objects.all()), 1)
        self.assertEqual(len(StockChangeSet.objects.all()), 1)
        self.assertEqual(len(StockChange.objects.all()), 1)

        # (Try to) add 1 article with cost 1 dollar
        entries = [{
            'article': art,
            'book_value': cost_usd,
            'count': 1,
            'is_in': True
        }]
        try:
            StockChangeSet.construct(description="AddDollarStock", entries=entries, enum=1)
        except CurrencyInconsistencyError:
            i = 1

        # Check if the CurrencyInconsistencyError occurred
        self.assertEqual(i, 1)

        # Check if there are no additional lines in the StockChangeSet and  stockchanges
        # The error should have rolled back the changes the second modification might have made
        self.assertEqual(len(StockChangeSet.objects.all()), 1)
        self.assertEqual(len(StockChange.objects.all()), 1)
        # Try to add another item with a price of 1 euro
        entries = [{
            'article': art,
            'book_value': cost_eur,
            'count': 1,
            'is_in': True
        }]

        i = 0

        try:
            StockChangeSet.construct(description="AddSecondEuroStock", entries=entries, enum=1)
        except CurrencyInconsistencyError:
            i = 1

        # This should have worked, so i should still be 0
        self.assertEqual(i, 0)

        # Check if the stock has indeed changed
        self.assertEqual(len(StockChangeSet.objects.all()), 2)
        self.assertEqual(len(StockChange.objects.all()), 2)

    def testToZero(self):
        """
        Test that tries to sell 6 items with increasing book value from an empty stock.
        """
        # Create some objects to use in the tests
        i = 0
        cur = Currency("EUR")
        vat = VAT.objects.create(vatrate=Decimal("1.21"), name="HIGH", active=True)
        art = ArticleType.objects.create(name="Product1", vat=vat)

        for i in range(1, 7):  # 1 to 6. Average should be 3.5
            # Define book value
            book_value = Cost(amount=Decimal(str(i)), currency=cur)

            # Construct entry for StockChangeSet
            entries = [{
                'article': art,
                'book_value': book_value,
                'count': 1,
                'is_in': True
            }]

            StockChangeSet.construct(description="AddSecondEuroStock", entries=entries, enum=1)
        for i in range(1, 7):  # 1 to 6. Average should be 3.5
            # Define book value
            book_value = Cost(amount=Decimal(str(i)), currency=cur)

            # Construct entry for StockChangeSet
            if settings.FORCE_NEGATIVE_STOCKCHANGES_TO_MAINTAIN_COST:
                book_value._amount = Decimal(3.5000)
            entries = [{
                    'article': art,
                    'book_value': book_value,
                    'count': 1,
                    'is_in': False
            }]
            StockChangeSet.construct(description="AddSecondEuroStock", entries=entries, enum=1)
        entries = [{
            'article': art,
            'book_value': book_value,
            'count': 0,
            'is_in': False
        }]
        StockChangeSet.construct(description="AddSecondEuroStock", entries=entries, enum=1)
        self.assertEqual(len(StockChange.objects.all_without_label()), 13)
        self.assertEqual(len(StockChange.objects.all_without_label()), 13)

        self.assertEqual(len(StockChange.objects.all()), 13)
        st = Stock.objects.all()
        if DELETE_STOCK_ZERO_LINES:
            self.assertEqual(st.__len__(), 0)
        else:
            self.assertEqual(st.__len__(), 1)

@StockLabel.register
class ZStockLabel(StockLabel):
    _labeltype="Zz"


@StockLabel.register
class TestStockLabel(StockLabel):
    _labeltype="test"


class ForgottenStockLabel(StockLabel):
    _labeltype="forgotten"


class LabelTest(TestCase):
    def setUp(self):
        self.eur = Currency("EUR")

        self.vat = VAT.objects.create(vatrate=Decimal("1.21"), name="HIGH", active=True)
        self.cost_eur = Cost(amount=Decimal(str(1)), currency=self.eur)  # 1 euro

        self.def_art = ArticleType.objects.create(name="P1", vat=self.vat)
        self.label1a = ZStockLabel(1)

        self.def_entries = entries = [{
            'article': self.def_art,
            'book_value': self.cost_eur,
            'count': 1,
            'is_in': True,
            'label': self.label1a
        }]

    def tearDown(self):

        self.assertEqual(Stock.do_check(),[])

    def testBasicLabel(self):
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
            'is_in': True,
            'label': self.label1a
        }]
        StockChangeSet.construct(description="AddSecondEuroStock", entries=entries, enum=1)
        StockChangeSet.construct(description="AddSecondEuroStock", entries=entries, enum=1)

        self.assertEqual(len(StockChange.objects.filter(label=self.label1a)), 2)
        self.assertEqual(len(StockChange.objects.all_without_label()), 0)
        self.assertEqual(len(StockChange.objects.all()), 2)
        self.assertEqual(len(Stock.objects.all()), 1)
        t = TestStockLabel(4)

        entries[0]["label"]=t
        StockChangeSet.construct(description="AddSecondEuroStock", entries=entries, enum=1)
        entries[0]["label"]=None
        StockChangeSet.construct(description="AddSecondEuroStock", entries=entries, enum=1)

    def raisesTest(self):
        StockChangeSet.construct(description="AddSecondEuroStock", entries=self.entries, enum=1)

    def testLabelFailBecauseNoLabel(self):
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
            'is_in': True,
            'label': self.label1a
        }]
        StockChangeSet.construct(description="AddSecondEuroStock", entries=entries, enum=1)
        self.entries = [{
            'article': art,
            'book_value': cost_eur,
            'count': 1,
            'is_in': False,
        }]
        self.assertRaises(StockSmallerThanZeroError, self.raisesTest)
        self.assertEqual(Stock.objects.get(label=self.label1a).count,1)
        self.assertEqual(StockChange.objects.all().__len__(),1)
        entries[0]['is_in']=False
        StockChangeSet.construct(description="AddSecondEuroStock", entries=entries, enum=1)
        if DELETE_STOCK_ZERO_LINES:
            self.assertEqual(Stock.objects.filter(label=self.label1a).__len__(), 0)
        else:
            self.assertEqual(Stock.objects.filter(label=self.label1a).__len__(), 1)

        self.entries = entries
        self.assertRaises(StockSmallerThanZeroError, self.raisesTest)
        self.assertEqual(StockChange.objects.all().__len__(),2)
        if DELETE_STOCK_ZERO_LINES:
            self.assertEqual(Stock.objects.filter(label=self.label1a).__len__(), 0)
        else:
            self.assertEqual(Stock.objects.filter(label=self.label1a).__len__(), 1)

    def raise_Invalid_Label_type_added(self):
        StockLabel.register(self.labeltype)

    def testTestLabelWithoutName(self):
        class InValidLabel(StockLabel):
            _labeltype = ""

        self.labeltype=InValidLabel
        self.assertRaises(ValueError, self.raise_Invalid_Label_type_added)
        self.assertEqual(StockLabel.labeltypes.get("", None), None)

    #Test what happens to the stock state if one line of stock is moved.
    def testMoveStock(self):

        # Add 1 article with cost 1 euro
        entries = self.def_entries

        StockChangeSet.construct(description="AddFirstStock", entries=entries, enum=1)
        self.assertEqual(StockChange.objects.all().__len__(), 1)
        self.assertEqual(Stock.objects.all().__len__(), 1)
        self.assertEqual(Stock.objects.all_without_label().__len__(),0)
        entries = [{
            'article': self.def_art,
            'book_value': self.cost_eur,
            'count': 1,
            'is_in': True,
            'label': None
        }, {
            'article': self.def_art,
            'book_value': self.cost_eur,
            'count': 1,
            'is_in': False,
            'label': self.label1a
        }]
        StockChangeSet.construct(description="AddSecondStock", entries=entries, enum=1)
        self.assertEqual(StockChange.objects.all().__len__(), 3)
        if DELETE_STOCK_ZERO_LINES:
            self.assertEqual(Stock.objects.all().__len__(), 1)
        else:
            self.assertEqual(Stock.objects.all().__len__(), 2)
        self.assertEqual(Stock.objects.all_without_label().__len__(),1)

    def testStockChangeCreateWithLabelTypeInsteadOfLabel(self):
        # Add 1 article with cost 1 euro
        self.entries = self.def_entries
        self.entries[0]['label'] = None
        self.entries[0]['labeltype'] = "TEST"
        self.assertRaises(ValueError, self.raisesTest)

    def testAverageStock(self):
        entries = [{
            'article': self.def_art,
            'book_value': self.cost_eur,
            'count': 1,
            'is_in': True,
            'label': None
        },{
            'article': self.def_art,
            'book_value': self.cost_eur,
            'count': 2,
            'is_in': True,
            'label': self.label1a
        }]
        StockChangeSet.construct(description="AddSecondStock", entries=entries, enum=1)
        self.cost_eur = self.cost_eur + self.cost_eur
        entries = [{
            'article': self.def_art,
            'book_value': self.cost_eur,
            'count': 1,
            'is_in': True,
            'label': None
        },{
            'article': self.def_art,
            'book_value': self.cost_eur,
            'count': 1,
            'is_in': True,
            'label': self.label1a
        }]
        StockChangeSet.construct(description="AddSecondStock", entries=entries, enum=1)
        without_label = Stock.objects.all_without_label()
        without_line = without_label[0]
        self.assertEqual(without_label.__len__(),1)
        with_label = Stock.objects.filter(label=self.label1a)
        self.assertEqual(with_label.__len__(),1)
        with_line = with_label[0]
        self.assertEqual(without_line.book_value.amount, Decimal("1.50000"))
        self.assertEqual(with_line.book_value.amount, Decimal("1.33333"))
        self.assertEqual(with_line.count,3)
        self.assertEqual(without_line.count,2)
        self.assertEqual(with_line.label,self.label1a)
        self.assertEqual(without_line.label,None)

    # THis function is NOT in accordance with how stock should be used, and is only used to verify uniqueness constraints on stock
    def newDirectStockLine(self):
        try:
            # Indirect=True is only used for this test, DO NOT USE THIS ELSEWHERE.
            Stock(article=self.def_art,book_value=self.cost_eur,count=2, label=self.label1a).save(indirect=True)
            return True
        except Exception:
            return False
    @skip
    def testMultipleStockLinesWithSameLabel(self):
        self.newDirectStockLine()
        a = self.newDirectStockLine()
        self.assertFalse(a)

    def create_forgotten_stock(self):
        return Stock(article=self.def_art,book_value=self.cost_eur,count=2, label=ForgottenStockLabel(4)).save(indirect=True)

    def testStockLabelNotRegistred(self):
        self.assertRaises(StockLabelNotFoundError, self.create_forgotten_stock)

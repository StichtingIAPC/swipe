from django.test import TestCase
from article.tests import INeedSettings
from money.models import Currency, Cost, Money, VAT, Price, AccountingGroup
from register.models import SalesPeriod, InactiveError
from decimal import Decimal
from article.models import ArticleType
from sales.models import SalesTransactionLine, Payment, Transaction
from stock.models import StockChange, StockSmallerThanZeroError, StockChangeSet
from register.models import PaymentType

# Create your tests here.
class TestTransactionNoSalesPeriod(INeedSettings, TestCase):
    def setUp(self):
        super().setUp()
        self.EUR = Currency("EUR")
        self.cost = Cost(Decimal("1.21000"), self.EUR)
        self.money = Money(Decimal("1.21000"), self.EUR)
        self.pt = PaymentType.objects.create()
        self.vat = VAT.objects.create(vatrate=Decimal("1.21"), name="HIGH", active=True)
        self.price = Price(Decimal("1.21000"), vat=self.vat.vatrate, currency=self.EUR)
        self.acc_group = AccountingGroup.objects.create(vat_group=self.vat, accounting_number=1, name='hoihoi')
        self.art = ArticleType.objects.create(name="P1", branch=self.branch,
                                              accounting_group=self.acc_group)

        self.simplest = SalesTransactionLine(article=self.art, count=1, cost=self.cost, price=self.price, num=1)
        self.simple_payment = Payment(amount=self.money, payment_type=self.pt)

    def do_transaction(self):
        Transaction.construct([self.simple_payment], [self.simplest])

    def test_simple(self):
        SalesTransactionLine(article=self.art, count=1, cost=self.cost, price=self.price, num=1)
        Payment(amount=self.money)
        StockChangeSet.construct("HENK", [{
            'article': self.art,
            'book_value': self.cost,
            'count': 1,
            'is_in': True,
        }], 1)
        self.assertRaises(InactiveError, self.do_transaction)
        self.assertEqual(1, StockChange.objects.all().__len__())
        self.assertEqual(0, Payment.objects.all().__len__())


class TestTransaction(INeedSettings, TestCase):
    def setUp(self):
        super().setUp()
        self.EUR = Currency("EUR")
        self.cost = Cost(Decimal("1.21000"), self.EUR)
        self.money = Money(Decimal("1.21000"), self.EUR)
        self.pt = PaymentType.objects.create()
        self.vat = VAT.objects.create(vatrate=Decimal("1.21"), name="HIGH", active=True)
        self.price = Price(Decimal("1.21000"), vat=self.vat.vatrate, currency=self.EUR)
        self.acc_group = AccountingGroup.objects.create(vat_group=self.vat, accounting_number=1, name='hoihoi')
        self.art = ArticleType.objects.create(name="P1", branch=self.branch,
                                              accounting_group=self.acc_group)
        self.art = ArticleType.objects.create(name="P1", branch=self.branch,
                                              accounting_group=self.acc_group)
        self.sp = SalesPeriod.objects.create()
        self.simplest = SalesTransactionLine(article=self.art, count=1, cost=self.cost, price=self.price, num=1)
        self.simple_payment = Payment(amount=self.money, payment_type=self.pt)

    def do_transaction(self):
        Transaction.construct([self.simple_payment], [self.simplest])

    def test_simple(self):
        SalesTransactionLine(article=self.art, count=1, cost=self.cost, price=self.price, num=1)
        Payment(amount=self.money)
        StockChangeSet.construct("HENK", [{
            'article': self.art,
            'book_value': self.cost,
            'count': 1,
            'is_in': True,
        }], 1)
        self.do_transaction()
        self.assertEqual(2, StockChange.objects.all().__len__())
        self.assertEqual(1, Payment.objects.all().__len__())

    def test_fail_no_stock(self):
        SalesTransactionLine(article=self.art, count=1, cost=self.cost, price=self.price, num=1)
        Payment(amount=self.money, payment_type=self.pt)
        self.assertRaises(StockSmallerThanZeroError, self.do_transaction)
        self.assertEqual(0, StockChange.objects.all().__len__())
        self.assertEqual(0, Payment.objects.all().__len__())

    def test_fail_no_consistent_pay(self):
        self.simple_payment = Payment(amount=self.money * 2)
        StockChangeSet.construct("HENK", [{
            'article': self.art,
            'book_value': self.cost,
            'count': 1,
            'is_in': True,
        }], 1)
        # A payment with different amount of Payment than products should FAIL
        self.assertRaises(AssertionError, self.do_transaction)
        self.assertEqual(1, StockChange.objects.all().__len__())
        self.assertEqual(0, Payment.objects.all().__len__())
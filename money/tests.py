from decimal import Decimal

from django.test import TestCase

# Create your tests here.
from money.models import Currency, TestSalesPriceType, SalesPrice
from money.models import TestMoneyType
from money.models import Money
from money.models import Cost
from money.models import TestCostType
from money.models import Price
from money.models import TestPriceType


class MoneyTest(TestCase):
    def setUp(self):
        c = Currency('EUR')
        m = Money(Decimal("5.21"), c)
        t = TestMoneyType.objects.create(money=m)

    def testMoneyStorage(self):
        val = TestMoneyType.objects.all()
        i = 0
        for v in val:
            self.assertEqual(type(v.money), Money)

            self.assertEqual(v.money.amount.__str__(), "5.21000")
            self.assertEqual(v.money.currency, Currency('EUR'))
            i += 1
        self.assertEqual(i, 1)


class CostTest(TestCase):
    def setUp(self):
        c = Currency('EUR')
        m = Cost(Decimal("5.21"), c)
        t = TestCostType.objects.create(cost=m)

    def testMoneyStorage(self):
        val = TestCostType.objects.all()
        i = 0
        for v in val:
            self.assertEqual(type(v.cost), Cost)
            self.assertEqual(v.cost.amount.__str__(), "5.21000")
            self.assertEqual(v.cost.currency, Currency('EUR'))
            i += 1

        self.assertEqual(i, 1)


class PriceTest(TestCase):
    def setUp(self):
        c = Currency('EUR')
        m = Price(amount=Decimal("5.21"), currency=c, vat=Decimal("1.21"))
        t = TestPriceType.objects.create(price=m)

    def testMoneyStorage(self):
        val = TestPriceType.objects.all()
        i = 0
        for v in val:
            self.assertEqual(type(v.price), Price)
            self.assertEqual(v.price.amount.__str__(), "5.21000")
            self.assertEqual(v.price.vat.__str__(), "1.210000")
            self.assertEqual(v.price.currency, Currency('EUR'))
            i += 1

        self.assertEqual(i, 1)


class SalesPriceTest(TestCase):
    def setUp(self):
        c = Currency('EUR')
        m = SalesPrice(amount=Decimal("5.21"), currency=c, vat=Decimal("1.93"), cost=Decimal("4.00"))

        t = TestSalesPriceType.objects.create(price=m)

    def testMoneyStorage(self):
        val = TestSalesPriceType.objects.all()
        i = 0
        for v in val:
            self.assertEqual(type(v.price), SalesPrice)
            self.assertEqual(v.price.amount.__str__(), "5.21000")
            self.assertEqual(v.price.cost.__str__(), "4.00000")
            self.assertEqual(v.price.vat.__str__(), "1.930000")
            self.assertEqual(v.price.currency, Currency('EUR'))
            i += 1

        self.assertEqual(i, 1)


class MoneyMathTest(TestCase):
    def setUp(self):
        eur = Currency("EUR")
        usd = Currency("USD")
        self.m1 = Money(amount=Decimal("1.00000"), currency=eur)
        self.m2 = Money(amount=Decimal("0.50000"), currency=eur)
        self.m3 = Cost(amount=Decimal("3.00000"), currency=usd)
        self.num = 4

    def testMoneyAdd(self):
        self.assertEquals((self.m1 + self.m2).amount.__str__(), "1.50000")
        t = False
        try:
            self.m2 + self.m3
        except TypeError:
            t = True
        self.assertTrue(t)
        t = False
        try:
            self.m2 + self.num
        except TypeError:
            t = True
        self.assertTrue(t)

    def testMoneyMult(self):
        eur = Currency("EUR")
        # Multiplying money times integer is valid
        self.assertEquals((self.m1 * self.num).amount.__str__(), "4.00000")
        t = False
        try:
            self.m2 * self.m3
        # Multiplying money times money is wrong
        except TypeError:
            t = True
        self.assertTrue(t)

    def testMoneySub(self):
        self.assertEquals((self.m1 - self.m2).amount.__str__(), "0.50000")
        t = False
        try:
            self.m2 - self.m3
        except TypeError:
            t = True
        self.assertTrue(t)
        t = False
        try:
            self.m2 - self.num
        except TypeError:
            t = True
        self.assertTrue(t)


# Copy of MoneyMathTest; they are not exactly the same
class CostMathTest(TestCase):
    def setUp(self):
        eur = Currency("EUR")
        usd = Currency("USD")
        self.m1 = Cost(amount=Decimal("1.00000"), currency=eur)
        self.m2 = Cost(amount=Decimal("0.50000"), currency=eur)
        self.m3 = Money(amount=Decimal("3.00000"), currency=usd)
        self.num = 4

    def testMoneyAdd(self):
        self.assertEquals((self.m1 + self.m2).amount.__str__(), "1.50000")
        self.assertEquals(type(self.m1 + self.m2), Cost)
        t = False
        try:
            self.m2 + self.m3
        except TypeError:
            t = True
        self.assertTrue(t)
        t = False
        try:
            self.m2 + self.num
        except TypeError:
            t = True
        self.assertTrue(t)

    def testMoneyMult(self):
        eur = Currency("EUR")
        # Multiplying money times integer is valid
        self.assertEquals((self.m1 * self.num).amount.__str__(), "4.00000")
        t = False
        try:
            self.m2 * self.m3
        # Multiplying money times money is wrong
        except TypeError:
            t = True
        self.assertTrue(t)

    def testMoneySub(self):
        self.assertEquals((self.m1 - self.m2).amount.__str__(), "0.50000")
        t = False
        try:
            self.m2 - self.m3
        except TypeError:
            t = True
        self.assertTrue(t)
        t = False
        try:
            self.m2 - self.num
        except TypeError:
            t = True
        self.assertTrue(t)


# Copy of MoneyMathTest; they are not exactly the same
class SalesPriceMathTest(TestCase):
    def setUp(self):
        eur = Currency("EUR")
        usd = Currency("USD")
        self.m1 = SalesPrice(amount=Decimal("1.00000"), currency=eur, vat=Decimal("1.21"), cost=Decimal("2.00000"))
        self.m2 = SalesPrice(amount=Decimal("0.50000"), currency=eur, vat=Decimal("1.21"), cost=Decimal("1.00000"))
        self.m3 = SalesPrice(amount=Decimal("2.00000"), currency=usd, vat=Decimal("1.21"), cost=Decimal("2.19000"))
        self.m4 = SalesPrice(amount=Decimal("0.50000"), currency=eur, vat=Decimal("1.06"), cost=Decimal("3.00000"))
        self.num = 4

    def testMoneyAdd(self):
        ans = self.m1 + self.m2

        self.assertEquals(ans.amount.__str__(), "1.50000")
        self.assertEquals(type(ans), SalesPrice)
        self.assertEquals(ans.cost.__str__(), "3.00000")
        self.wrong = [self.m3, self.m4, self.num]
        for w in self.wrong:
            i = 0
            try:
                self.m1 + w
            except TypeError:
                i = 1
            self.assertEqual(i, 1, "{} can't be added to SalesPrice".format(w))

    def testMoneySub(self):
        ans = self.m1 - self.m2
        self.assertEquals(ans.amount.__str__(), "0.50000")
        self.assertEquals(type(ans), SalesPrice)
        self.assertEquals(ans.cost.__str__(), "1.00000")
        self.wrong = [self.m3, self.m4, self.num]
        for w in self.wrong:
            i = 0
            try:
                self.m1 - w
            except TypeError:
                i = 1
            self.assertEqual(i, 1, "{} can't be subtracted from SalesPrice".format(w))

    def testMoneyMult(self):
        ans = self.m1 * self.num
        self.assertEquals(ans.amount.__str__(), "4.00000")
        self.assertEquals(type(ans), SalesPrice)
        self.assertEquals(ans.cost.__str__(), "8.00000")
        self.wrong = [self.m2, self.m3, self.m4]
        for w in self.wrong:
            i = 0
            try:
                self.m1 * w
            except TypeError:
                i = 1
            self.assertEqual(i, 1, "{} can't be multiplied with SalesPrice".format(w))

    def testSalesPriceMargin(self):
        t = SalesPrice(amount=Decimal("4.00000"), currency=Currency("EUR"), vat=Decimal("2"), cost=Decimal("0.50000"))
        self.assertEquals(t.get_profit(), 1.5)
        self.assertEquals(t.get_margin(), 3)

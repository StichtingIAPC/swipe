from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase, SimpleTestCase

from money.models import Cost
from money.models import Currency, TestSalesPriceType, SalesPrice
from money.models import CurrencyData
from money.models import Denomination
from money.models import Money
from money.models import Price
from money.models import TestCostType
from money.models import TestMoneyType
from money.models import TestPriceType
from swipe.settings import USED_CURRENCY


class MoneyTest(TestCase):
    def setUp(self):
        c = Currency('EUR')
        m = Money(Decimal("5.21"), c)
        TestMoneyType.objects.create(money=m)

    def testMoneyStorage(self):
        val = TestMoneyType.objects.all()
        i = 0
        for v in val:
            self.assertEqual(type(v.money), Money)

            self.assertEqual(v.money.amount.__str__(), "5.21000")
            self.assertEqual(v.money.currency, Currency('EUR'))
            i += 1
        self.assertEqual(i, 1)

    def testCreateMoneyWithoutCurency(self):
        m = Money(Decimal("5.21"), None, use_system_currency=True)
        self.assertEqual(m.currency, Currency(iso=USED_CURRENCY))


class CostTest(TestCase):
    def setUp(self):
        c = Currency('EUR')
        m = Cost(Decimal("5.21"), c)
        TestCostType.objects.create(cost=m)

    def testMoneyStorage(self):
        val = TestCostType.objects.all()
        i = 0
        for v in val:
            self.assertEqual(type(v.cost), Cost)
            self.assertEqual(v.cost.amount.__str__(), "5.21000")
            self.assertEqual(v.cost.currency, Currency('EUR'))
            i += 1

        self.assertEqual(i, 1)

    def testCreateCostWithoutCurrency(self):
        m = Cost(Decimal("5.21"), None, use_system_currency=True)
        self.assertEqual(m.currency, Currency(iso=USED_CURRENCY))


class PriceTest(TestCase):
    def setUp(self):
        c = Currency('EUR')
        m = Price(amount=Decimal("5.21"), vat=Decimal("1.21"), currency=c)
        TestPriceType.objects.create(price=m)

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

    def testCreatePriceWithoutCurrency(self):
        m = Price(amount=Decimal("5.21"), vat=Decimal("1.21"), currency=None, use_system_currency=True)
        self.assertEqual(m.currency, Currency(iso=USED_CURRENCY))


class SalesPriceTest(TestCase):
    def setUp(self):
        c = Currency('EUR')
        m = SalesPrice(amount=Decimal("5.21"), vat=Decimal("1.93"), currency=c, cost=Decimal("4"))
        TestSalesPriceType.objects.create(price=m)

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

    def testCreatePriceWithoutCurrency(self):
        m = SalesPrice(amount=Decimal("5.21"), vat=Decimal("1.93"), currency=None, cost=Decimal("4"),
                       use_system_currency=True)
        self.assertEqual(m.currency, Currency(iso=USED_CURRENCY))


class MoneyMathTest(SimpleTestCase):
    def setUp(self):
        eur = Currency("EUR")
        usd = Currency("USD")
        self.m1 = Money(amount=Decimal("1.00000"), currency=eur)
        self.m2 = Money(amount=Decimal("0.50000"), currency=eur)
        self.m3 = Cost(amount=Decimal("3.00000"), currency=usd)
        self.num = 4
        self.used = USED_CURRENCY

    def testMoneyAdd(self):
        self.assertEquals((self.m1 + self.m2).amount.__str__(), "1.50000")
        with self.assertRaises(TypeError):
            self.m2 + self.m3
        with self.assertRaises(TypeError):
            self.m2 + self.num

    def testMoneyMult(self):
        # Multiplying money times integer is valid
        self.assertEquals((self.m1 * self.num).amount.__str__(), "4.00000")
        with self.assertRaises(TypeError):
            self.m2 * self.m3
            # Multiplying money times money is wrong

    def testMoneySub(self):
        self.assertEquals((self.m1 - self.m2).amount.__str__(), "0.50000")
        with self.assertRaises(TypeError):
            self.m2 - self.m3
        with self.assertRaises(TypeError):
            self.m2 - self.num

    def test_uses_system_currency(self):
        v1 = Money(amount=Decimal("1"), currency=Currency(self.used))
        self.assertTrue(v1.uses_system_currency())
        fake_currency = "XXX"
        v2 = Money(amount=Decimal("1"), currency=Currency(fake_currency))
        self.assertFalse(v2.uses_system_currency())


# Copy of MoneyMathTest; they are not exactly the same
class CostMathTest(SimpleTestCase):
    def setUp(self):
        eur = Currency("EUR")
        usd = Currency("USD")
        self.m1 = Cost(amount=Decimal("1.00000"), currency=eur)
        self.m2 = Cost(amount=Decimal("0.50000"), currency=eur)
        self.m3 = Money(amount=Decimal("3.00000"), currency=usd)
        self.num = 4
        self.used = USED_CURRENCY

    def testMoneyAdd(self):
        self.assertEquals((self.m1 + self.m2).amount.__str__(), "1.50000")
        self.assertEquals(type(self.m1 + self.m2), Cost)
        with self.assertRaises(TypeError):
            self.m2 + self.m3
        with self.assertRaises(TypeError):
            self.m2 + self.num

    def testMoneyMult(self):
        # Multiplying money times integer is valid
        self.assertEquals((self.m1 * self.num).amount.__str__(), "4.00000")
        with self.assertRaises(TypeError):
            self.m2 * self.m3

    def testMoneySub(self):
        self.assertEquals((self.m1 - self.m2).amount.__str__(), "0.50000")
        with self.assertRaises(TypeError):
            self.m2 - self.m3
        with self.assertRaises(TypeError):
            self.m2 - self.num

    def test_subtype_uses_system_currency(self):
        v1 = Cost(amount=Decimal("1"), currency=Currency(self.used))
        self.assertTrue(v1.uses_system_currency())
        fake_currency = "XXX"
        v2 = Cost(amount=Decimal("1"), currency=Currency(fake_currency))
        self.assertFalse(v2.uses_system_currency())

# Copy of MoneyMathTest; they are not exactly the same

class SalesPriceMathTest(SimpleTestCase):
    def setUp(self):
        eur = Currency("EUR")
        usd = Currency("USD")
        self.m1 = SalesPrice(amount=Decimal("1.00000"), vat=Decimal("1.21"), currency=eur, cost=Decimal("2.00000"))
        self.m2 = SalesPrice(amount=Decimal("0.50000"), vat=Decimal("1.21"), currency=eur, cost=Decimal("1.00000"))
        self.m3 = SalesPrice(amount=Decimal("2.00000"), vat=Decimal("1.21"), currency=usd, cost=Decimal("0.00000"))
        self.m4 = SalesPrice(amount=Decimal("0.50000"), vat=Decimal("1.06"), currency=eur, cost=Decimal("0.00000"))
        self.num = 4

    def testMoneyAdd(self):
        ans = self.m1 + self.m2

        self.assertEquals(ans.amount.__str__(), "1.50000")
        self.assertEquals(type(ans), SalesPrice)
        self.assertEquals(ans.cost.__str__(), "3.00000")
        self.wrong = [self.m3, self.m4, self.num]
        for w in self.wrong:
            with self.assertRaises(TypeError, msg="{} can't be added to SalesPrice".format(w)):
                self.m1 + w

    def testMoneySub(self):
        ans = self.m1 - self.m2
        self.assertEquals(ans.amount.__str__(), "0.50000")
        self.assertEquals(type(ans), SalesPrice)
        self.assertEquals(ans.cost.__str__(), "1.00000")
        self.wrong = [self.m3, self.m4, self.num]
        for w in self.wrong:
            with self.assertRaises(TypeError, msg="{} can't be subtracted from SalesPrice".format(w)):
                self.m1 - w

    def testMoneyMult(self):
        ans = self.m1 * self.num
        self.assertEquals(ans.amount.__str__(), "4.00000")
        self.assertEquals(type(ans), SalesPrice)
        self.assertEquals(ans.cost.__str__(), "8.00000")
        self.wrong = [self.m2, self.m3, self.m4]
        for w in self.wrong:
            with self.assertRaises(TypeError, msg="{} can't be multiplied with SalesPrice".format(w)):
                self.m1 * w

    def testSalesPriceMargin(self):
        t = SalesPrice(amount=Decimal("4.00000"), vat=Decimal("2"), currency=Currency("EUR"), cost=Decimal("0.5"))
        self.assertEquals(t.get_profit(), 1.5)
        self.assertEquals(t.get_margin(), 3)


class CurrencyDenomDBTest(TestCase):

    def test_currency_iso(self):
        with self.assertRaises(ValidationError):
            foo = CurrencyData(iso="EADD", name="Estonian Drak", digits=4, symbol="D&")
            foo.full_clean()

    def test_currency_symbol(self):
        with self.assertRaises(ValidationError):
            foo = CurrencyData(iso="EDD", name="Estonian Drak", digits=4, symbol="D&aaaa")
            foo.full_clean()


class CurrencyDenomTest(SimpleTestCase):

    def setUp(self):
        self.euro = CurrencyData(iso="EUR", name="Euro", digits=2, symbol="€")
        self.dollar = CurrencyData(iso="USD", name="United States Dollar", digits=2, symbol="$")

    def test_currency_equals(self):
        self.assertNotEquals(self.euro, self.dollar)
        self.assertEquals(self.euro, self.euro)
        self.assertNotEquals(self.euro, 4)

    def test_denomination_currency(self):
        self.denom1 = Denomination(currency=self.euro, amount=2.2)
        self.denom2 = Denomination(currency=self.euro, amount=2.2)
        self.assertTrue(self.denom1.has_same_currency(self.denom2))

    def test_denomination_equals(self):
        self.denom1 = Denomination(currency=self.euro, amount=2.2)
        self.denom2 = Denomination(currency=self.euro, amount=2.2)
        self.denom3 = Denomination(currency=self.dollar, amount=2.2)
        self.assertEquals(self.denom1, self.denom2)
        self.assertNotEqual(self.denom1, self.denom3)

    def test_denom_srt(self):
        denom1 = Denomination(currency=self.euro, amount=2.2)
        self.assertEquals(str(denom1), "EUR 2.2")

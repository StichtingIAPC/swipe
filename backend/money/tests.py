from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase, SimpleTestCase
from tools.testing import TestData
import datetime

from money.models import Cost
from money.models import Currency, TestSalesPriceType, SalesPrice
from money.models import CurrencyData
from money.models import Denomination
from money.models import Money, VAT, VATPeriod, VATError
from money.models import Price, InvalidDataError
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

    def testCreatingMoneyWithCurrencyDataFails(self):
        with self.assertRaises(InvalidDataError):
            Money(amount=Decimal(0), currency=CurrencyData(iso="EUR", name="Euro", digits=2, symbol="€"))

    def testCreatingMoneyWithNonDecimalFails(self):
        with self.assertRaises(InvalidDataError):
            Money(amount=1, currency=Currency("EUR"))


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


# noinspection PyUnresolvedReferences
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
# noinspection PyUnresolvedReferences
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

    def test_cost_div_by_int(self):
        self.assertEqual(self.m1 / 2, self.m2)

    def test_cost_div_by_cost(self):
        self.assertEqual(self.m2 / self.m1, Decimal("0.5"))

    def test_subtype_uses_system_currency(self):
        v1 = Cost(amount=Decimal("1"), currency=Currency(self.used))
        self.assertTrue(v1.uses_system_currency())
        fake_currency = "XXX"
        v2 = Cost(amount=Decimal("1"), currency=Currency(fake_currency))
        self.assertFalse(v2.uses_system_currency())


# Copy of MoneyMathTest; they are not exactly the same

# noinspection PyUnresolvedReferences,PyUnresolvedReferences
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


class VATTests(TestCase, TestData):
    def test_no_period_is_incorrect(self):
        v1 = VAT(name="VATFoo", active=True)
        v1.save()
        with self.assertRaises(VATError):
            v1.getvatrate()

    def test_period_overlap_is_incorrect(self):
        v1 = VAT(name="VATFoo", active=True)
        v1.save()
        date_1 = datetime.datetime.strptime('01012010', "%d%m%Y").date()
        date_2 = datetime.datetime.strptime('01012030', "%d%m%Y").date()
        date_3 = datetime.datetime.strptime('01012031', "%d%m%Y").date()
        vp1 = VATPeriod(vat=v1, begin_date=date_1, end_date=date_2, vatrate=Decimal("1"))
        vp1.save()
        vp2 = VATPeriod(vat=v1, begin_date=date_1, end_date=date_3, vatrate=Decimal("1"))
        with self.assertRaises(VATError):
            vp2.save()

    def test_one_period_bounded_works(self):
        v1 = VAT(name="VATFoo", active=True)
        v1.save()
        rate = Decimal("1.1")
        date_1 = datetime.datetime.strptime('01012010', "%d%m%Y").date()
        date_2 = datetime.datetime.strptime('01012030', "%d%m%Y").date()
        vp1 = VATPeriod(vat=v1, begin_date=date_1, end_date=date_2, vatrate=rate)
        vp1.save()
        r = v1.getvatrate()
        self.assertAlmostEqual(r, rate)

    def test_one_period_unbounded_works(self):
        v1 = VAT(name="VATFoo", active=True)
        v1.save()
        rate = Decimal("1.1")
        date_1 = datetime.datetime.strptime('01012010', "%d%m%Y").date()
        vp1 = VATPeriod(vat=v1, begin_date=date_1, vatrate=rate)
        vp1.save()
        r = v1.getvatrate()
        self.assertEqual(r, rate)

    def test_two_periods_work(self):
        v1 = VAT(name="VATFoo", active=True)
        v1.save()
        date_1 = datetime.datetime.strptime('01012010', "%d%m%Y").date()
        date_2 = datetime.datetime.strptime('01012011', "%d%m%Y").date()
        date_3 = datetime.datetime.strptime('02012011', "%d%m%Y").date()
        date_4 = datetime.datetime.strptime('01012031', "%d%m%Y").date()
        rate_1 = Decimal("1.1")
        rate_2 = Decimal("1.2")
        vp1 = VATPeriod(vat=v1, begin_date=date_1, end_date=date_2, vatrate=rate_1)
        vp1.save()
        vp2 = VATPeriod(vat=v1, begin_date=date_3, end_date=date_4, vatrate=rate_2)
        vp2.save()
        r = v1.getvatrate()
        self.assertEqual(r, rate_2)

    def test_bounds_are_taken_exactly_at_end(self):
        v1 = VAT(name="VATFoo", active=True)
        v1.save()
        date_1 = datetime.datetime.strptime('01012010', "%d%m%Y").date()
        date_2 = datetime.date.today()
        date_3 = datetime.date.today() + datetime.timedelta(days=1)
        date_4 = datetime.datetime.strptime('01012031', "%d%m%Y").date()
        rate_1 = Decimal("1.1")
        rate_2 = Decimal("1.2")
        vp1 = VATPeriod(vat=v1, begin_date=date_1, end_date=date_2, vatrate=rate_1)
        vp1.save()
        vp2 = VATPeriod(vat=v1, begin_date=date_3, end_date=date_4, vatrate=rate_2)
        vp2.save()
        r = v1.getvatrate()
        self.assertEqual(r, rate_1)

    def test_bounds_are_taken_exactly_at_beginning(self):
        v1 = VAT(name="VATFoo", active=True)
        v1.save()
        date_1 = datetime.datetime.strptime('01012010', "%d%m%Y").date()
        date_2 = datetime.date.today() - datetime.timedelta(days=1)
        date_3 = datetime.date.today()
        date_4 = datetime.datetime.strptime('01012031', "%d%m%Y").date()
        rate_1 = Decimal("1.1")
        rate_2 = Decimal("1.2")
        vp1 = VATPeriod(vat=v1, begin_date=date_1, end_date=date_2, vatrate=rate_1)
        vp1.save()
        vp2 = VATPeriod(vat=v1, begin_date=date_3, end_date=date_4, vatrate=rate_2)
        vp2.save()
        r = v1.getvatrate()
        self.assertEqual(r, rate_2)

    def test_new_vat_period_without_end_can_conflict_with_old_vat_period(self):
        v1 = VAT(name="VATFoo", active=True)
        v1.save()
        date_1 = datetime.datetime.strptime('01012010', "%d%m%Y").date()
        date_2 = datetime.datetime.strptime('01012030', "%d%m%Y").date()
        date_3 = datetime.datetime.strptime('01022011', "%d%m%Y").date()
        vp1 = VATPeriod(vat=v1, begin_date=date_1, end_date=date_2, vatrate=Decimal("1"))
        vp1.save()
        vp2 = VATPeriod(vat=v1, begin_date=date_3, end_date=None, vatrate=Decimal("1"))
        with self.assertRaises(VATError):
            vp2.save()

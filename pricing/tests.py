from django.test import TestCase, SimpleTestCase
from django.db.utils import IntegrityError
from tools.testing import TestData
from pricing.models import PricingModel, PricingError, Rounding
from money.models import Price, Cost
from django.core.exceptions import ValidationError
from decimal import Decimal
from stock.models import StockChangeSet, Stock


class PriorityTests(TestCase, TestData):

    def setUp(self):
        self.setup_base_data()

    def test_uniqueness(self):
        p1 = PricingModel(function_identifier=1, name="Foo", position=1)
        p2 = PricingModel(function_identifier=2, name="Bar", position=1, margin=Decimal("1.085"))
        p1.save()
        with self.assertRaises(IntegrityError):
            p2.save()

    def test_position_bigger_than_0(self):
        p1 = PricingModel(function_identifier=1, name="Foo", position=-1)
        with self.assertRaises(ValidationError):
            p1.save()

    def test_priority_is_followed_margin_first(self):
        pm1 = PricingModel(function_identifier=1, name="Fixed Price", position=2)
        pm2 = PricingModel(function_identifier=2, name="Fixed Margin", position=1, margin=Decimal(1))
        pm1.save()
        pm2.save()

        price = Price(amount=Decimal("100"), use_system_currency=True, vat=self.articletype_1.get_vat_rate())
        self.articletype_1.fixed_price = price
        self.articletype_1.save()

        price_found = PricingModel.return_price(self.articletype_1)
        price_expected = Price(amount=Rounding.round_up(self.cost_system_currency_1.amount*self.articletype_1.get_vat_rate()), currency=self.cost_system_currency_1.currency,
                               vat=self.articletype_1.get_vat_rate())
        self.assertEqual(price_found.amount, price_expected.amount)

    def test_priority_is_followed_fixed_first(self):
        pm1 = PricingModel(function_identifier=1, name="Fixed Price", position=1)
        pm2 = PricingModel(function_identifier=2, name="Fixed Margin", position=2)
        pm1.save()
        pm2.save()

        price = Price(amount=Decimal("100"), use_system_currency=True, vat=self.articletype_1.get_vat_rate())
        self.articletype_1.fixed_price = price
        self.articletype_1.save()

        price_found = PricingModel.return_price(self.articletype_1, margin=Decimal(1))
        price_expected = Price(amount= Decimal("100"), currency=self.cost_system_currency_1.currency,
                               vat=self.articletype_1.get_vat_rate())
        self.assertEqual(price_found, price_expected)


class RoundingTests(SimpleTestCase):

    def test_round_smaller_than_1_does_round_up(self):
        unrounded = Decimal("0.96")
        rounded = Rounding.round_up(unrounded)
        self.assertEqual(rounded, Decimal("1"))

    def test_round_smaller_then_1_also_rounds_up(self):
        unrounded = Decimal("0.98")
        rounded = Rounding.round_up(unrounded)
        self.assertEqual(rounded, Decimal("1"))

    def test_rounded_value_smeq_1_does_not_round_away(self):
        already_rounded = Decimal("0.95")
        rounded = Rounding.round_up(already_rounded)
        self.assertEqual(rounded, Decimal("0.95"))

    def test_rounding_bigger_than_1_smaller_than_15(self):
        unrounded = Decimal("1.01")
        rounded = Rounding.round_up(unrounded)
        self.assertEqual(rounded, Decimal("1.2"))

    def test_rounding_bigger_than_1_rounds_up(self):
        unrounded = Decimal("1.11")
        rounded = Rounding.round_up(unrounded)
        self.assertEqual(rounded, Decimal("1.2"))

    def test_rounding_bigger_than_15(self):
        unrounded = Decimal("15.01")
        rounded = Rounding.round_up(unrounded)
        self.assertEqual(rounded, Decimal("15.5"))

    def test_rounding_bigger_than_15_rounds_ok(self):
        unrounded = Decimal("15.26")
        rounded = Rounding.round_up(unrounded)
        self.assertEqual(rounded, Decimal("15.5"))


class PricingTests(TestCase, TestData):

    def setUp(self):
        self.setup_base_data()

    def test_no_pricing_rows_fails(self):
        with self.assertRaises(PricingError):
            PricingModel.return_price(self.articletype_1)

    def test_pricing_model_processing(self):
        pm1 = PricingModel(function_identifier=1, name="Fixed Price", position=1)
        pm1.save()
        price = Price(amount=Decimal("1"), use_system_currency=True, vat=self.articletype_1.get_vat_rate())
        self.articletype_1.fixed_price = price
        self.articletype_1.save()
        price_found = PricingModel.return_price(self.articletype_1)
        self.assertEqual(price, price_found)

    def test_fixed_margin_stockless_article(self):
        pm1 = PricingModel(function_identifier=2, name="Fixed Margin", position=1, margin=Decimal(2))
        pm1.save()
        price_found = PricingModel.return_price(self.articletype_1)
        price_expected = Price(
            amount=Rounding.round_up(self.cost_system_currency_1.amount * Decimal(2) *
                                     self.articletype_1.get_vat_rate()),
            currency=self.cost_system_currency_1.currency,
            vat=self.articletype_1.get_vat_rate())
        self.assertEqual(price_found, price_expected)

    def test_fixed_margin_stock_article(self):
        pm1 = PricingModel(function_identifier=2, name="Fixed Margin", position=1, margin=Decimal(2))
        pm1.save()
        cst = Cost(amount=Decimal(10), use_system_currency=True)
        StockChangeSet.construct(description="None", entries=[
            {'article': self.articletype_1,
             'book_value': cst,
             'count': 3,
             'is_in': True}
        ], source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        st = Stock.objects.get()

        price_found = PricingModel.return_price(stock=st)
        price_expected = Price(amount=Rounding.round_up(Decimal(10)*Decimal(2)*self.articletype_1.get_vat_rate()),
                               use_system_currency=True, vat=self.articletype_1.get_vat_rate())
        self.assertEqual(price_expected, price_found)

    def test_fixed_margin_othercost(self):
        pm1 = PricingModel(function_identifier=2, name="Fixed Margin", position=1, margin=Decimal(2))
        pm1.save()
        price_found = PricingModel.return_price(sellable_type=self.othercosttype_1)
        price_expect = self.price_system_currency_1
        self.assertEqual(price_found.amount, price_expect.amount)
        self.assertAlmostEqual(price_found.vat, Decimal(price_expect.vat), 4)

    def test_fixed_margin_fallthrough_no_info(self):
        pm1 = PricingModel(function_identifier=2, name="Fixed Margin", position=1)
        pm1.save()
        with self.assertRaises(PricingError):
            PricingModel.return_price()

    def test_fixed_margin_fallthrough_no_margin(self):
        pm1 = PricingModel(function_identifier=2, name="Fixed Margin", position=1)
        pm1.save()
        with self.assertRaises(PricingError):
            PricingModel.return_price(sellable_type=self.articletype_1)

    def test_fixed_price_analyze_stock(self):
        pm1 = PricingModel(function_identifier=1, name="Fixed Price", position=1)
        pm1.save()
        price = Price(amount=Decimal("1"), use_system_currency=True, vat=self.articletype_1.get_vat_rate())
        self.articletype_1.fixed_price = price
        self.articletype_1.save()
        StockChangeSet.construct(description="None", entries=[
            {'article': self.articletype_1,
             'book_value': self.cost_system_currency_1,
             'count': 3,
             'is_in': True}
        ], source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        price_found = PricingModel.return_price(stock=Stock.objects.get())
        self.assertEqual(price_found, price)

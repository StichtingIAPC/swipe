from django.test import TestCase, SimpleTestCase
from django.db.utils import IntegrityError
from tools.testing import TestData
from pricing.models import PricingModel, PricingError, Rounding
from money.models import Price, Cost, Currency
from django.core.exceptions import ValidationError
from decimal import Decimal
from stock.models import StockChangeSet, Stock


class CalculatingPrice(TestCase, TestData):
    def setUp(self):
        self.setup_base_data()

    def test_calculate_price(self):
        self.assertEqual(Decimal("125.84000"), PricingModel.calc_price(Cost(Decimal(100), Currency("EUR")), Decimal("1.21"), None).amount)
        self.assertEqual(Decimal("1.41000"), PricingModel.calc_price(Cost(Decimal(1), Currency("EUR")), Decimal("1.21"), None).amount)

    def test_calculate_price_using_model(self):
        PricingModel.objects.create(exp_mult=Decimal(1), exponent=Decimal(0), constMargin=Decimal(0), min_relative_margin_error=0, max_relative_margin_error=0)
        self.assertEqual(Decimal("2.00000"), PricingModel.calc_price(Cost(Decimal(1), Currency("EUR")), Decimal("1"), None).amount)


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


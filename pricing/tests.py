from django.test import TestCase, SimpleTestCase
from django.db.utils import IntegrityError
from tools.testing import TestData
from pricing.models import PricingModel, PricingError, Rounding
from money.models import Price
from django.core.exceptions import ValidationError
from decimal import Decimal


class PriorityTests(TestCase, TestData):

    def setUp(self):
        self.setup_base_data()

    def test_uniqueness(self):
        p1 = PricingModel(name="Foo", position=1)
        p2 = PricingModel(name="Bar", position=1)
        p1.save()
        with self.assertRaises(IntegrityError):
            p2.save()

    def test_position_bigger_than_0(self):
        p1 = PricingModel(name="Foo", position=-1)
        with self.assertRaises(ValidationError):
            p1.save()


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

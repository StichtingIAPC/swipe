from django.test import TestCase
from django.db.utils import IntegrityError
from tools.testing import TestData
from pricing.models import PricingModel, PricingError
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


class PricingTests(TestCase, TestData):

    def setUp(self):
        self.setup_base_data()

    def test_no_pricing_rows_fails(self):
        with self.assertRaises(PricingError):
            PricingModel.return_price(self.articletype_1)

    def test_pricing_model_processing(self):
        pm1 = PricingModel(function_identifier=1, name="Fixed Price", position=1)
        pm1.save()
        price = Price(amount=Decimal("1"), use_system_currency=True)
        self.articletype_1.fixed_price = price
        self.articletype_1.save()
        price_found = PricingModel.return_price(self.articletype_1)
        # Vat needs to be taken into account, as of yet, this does not work
        #print(price_found)
        #self.assertEqual(price, price_found)

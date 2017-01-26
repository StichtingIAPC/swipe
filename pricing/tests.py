from django.test import TestCase
from django.db.utils import IntegrityError
from tools.testing import TestData
from pricing.models import PricingModel
from django.core.exceptions import ValidationError


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

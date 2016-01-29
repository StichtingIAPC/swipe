from django.test import TestCase

# Create your tests here.
from money.models import Currency
from money.models import TestMoneyType
from money.models import Money

class AnimalTestCase(TestCase):
    def setUp(self):
        c = Currency.objects.create(name="EURO",iso="EUR",symbol="$")
        TestMoneyType.objects.create(money=Money(c,5.25))
    def testSymbol(self):
        val = Currency.objects.get(name="EURO")
        self.assertEqual(val.iso,"EUR")
 #   def test_Euro(self):
  #      """Animals that can speak are correctly identified"""
#        val = TestMoneyType.objects.all()
#        i = 0
#        for v in val:
#            i += 1
#        self.assertEqual(i,1)

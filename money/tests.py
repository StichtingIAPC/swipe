from decimal import Decimal

from django.test import TestCase

# Create your tests here.
from money.models import Currency
from money.models import TestMoneyType
from money.models import Money

class CurrencyTest(TestCase):
    def setUp(self):
        c = Currency.objects.create(name="EURO",iso="EUR",symbol="$")
    def testSymbol(self):
        val = Currency.objects.get(name="EURO")
        self.assertEqual(val.iso,"EUR")


class MoneyTest(TestCase):
    def setUp(self):
        c = Currency.objects.create(name="EURO",iso="EUR",symbol="$")
        m = Money(amount=5.21,currency=c)

        t = TestMoneyType.objects.create(money=m)
        print(t.money.currency)

    def testSymbol(self):
        vv = Currency.objects.get(name="EURO")
        val = TestMoneyType.objects.all()
        i=0
        for v in val:
            self.assertEqual(v.money.amount.__str__(), "5.21000")
            self.assertEqual(v.money.currency,vv)


        self.assertEqual(vv.iso,"EUR")
 #   def test_Euro(self):
  #      """Animals that can speak are correctly identified"""
#        val = TestMoneyType.objects.all()
#        i = 0
#        for v in val:
#            i += 1
#        self.assertEqual(i,1)

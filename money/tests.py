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

        t = TestMoneyType.objects.create(money=m, name="Some Reason")
        print(t.money.currency)

    def testSymbol(self):
        vv = Currency.objects.get(iso="EUR")
        val = TestMoneyType.objects.get(name="Some Reason")
        self.assertEqual(val.money.amount.__str__(), "5.21000")
        self.assertEqual(val.money.currency,vv)


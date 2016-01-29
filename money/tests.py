from decimal import Decimal

from django.test import TestCase

# Create your tests here.
from money.models import Currency
from money.models import TestMoneyType
from money.models import Money

class MoneyTest(TestCase):
    def setUp(self):
        c = Currency('EUR')
        m = Money(amount=Decimal("5.21"),currency=c)

        t = TestMoneyType.objects.create(money=m, money_currency=c.iso)

    def testSymbol(self):
        val = TestMoneyType.objects.all()
        i=0
        for v in val:
            self.assertEqual(v.money.amount.__str__(), "5.21000")
            self.assertEqual(v.money.currency, Currency('EUR'))

            i+=1

 #   def test_Euro(self):
  #      """Animals that can speak are correctly identified"""
#        val = TestMoneyType.objects.all()
#        i = 0
#        for v in val:
#            i += 1
#        self.assertEqual(i,1)

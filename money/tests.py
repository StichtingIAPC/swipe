from decimal import Decimal

from django.test import TestCase

# Create your tests here.
from money.models import Currency
from money.models import TestMoneyType
from money.models import Money
from money.models import Cost
from money.models import TestCostType



class MoneyTest(TestCase):
    def setUp(self):
        c = Currency('EUR')
        m = Money(amount=Decimal("5.21"),currency=c)
        t = TestMoneyType.objects.create(money=m)
    def testMoneyStorage(self):
        val = TestMoneyType.objects.all()
        i=0
        for v in val:
            self.assertEqual(v.money.amount.__str__(), "5.21000")
            self.assertEqual(v.money.currency, Currency('EUR'))
            i=i+1
        self.assertEqual(i,1)


class CostTest(TestCase):
    def setUp(self):
        c = Currency('EUR')
        m = Cost(amount=Decimal("5.21"),currency=c)
        print(m)
        t = TestCostType.objects.create(money=m)

    def testMoneyStorage(self):
        val = TestCostType.objects.all()
        i=0
        for v in val:
            print(type(v.money))
            self.assertEqual(v.money.amount.__str__(), "5.21000")
            self.assertEqual(v.money.currency, Currency('EUR'))
            i=i+1

        self.assertEqual(i,1)

class MoneyMathTest(TestCase):
    def setUp(self):
        eur = Currency("EUR")
        usd = Currency("USD")
        self.m1 =  Money(amount=Decimal("1.00000"),currency=eur)
        self.m2 = Money(amount=Decimal("0.50000"),currency=eur)
        self.m3 = Money(amount=Decimal("3.00000"),currency=usd)
        self.num = 4

    def testMoneyAdd(self):
        self.assertEquals((self.m1+self.m2).amount.__str__(),"1.50000")
        t = False
        try:
            self.m2+self.m3
        except TypeError as err:
            t = True
        self.assertTrue(t)
        t = False
        try:
            self.m2+self.num
        except TypeError as err:
            t = True
        self.assertTrue(t)

    def testMoneyMult(self):
        eur = Currency("EUR")
        # Multiplying money times integer is valid
        self.assertEquals((self.m1*self.num).amount.__str__(),"4.00000")
        t = False
        try:
            self.m2*self.m3
        # Multiplying money times money is wrong
        except TypeError as err:
            t = True
        self.assertTrue(t)

    def testMoneySub(self):
        self.assertEquals((self.m1-self.m2).amount.__str__(),"0.50000")
        t = False
        try:
            self.m2-self.m3
        except TypeError as err:
            t = True
        self.assertTrue(t)
        t = False
        try:
            self.m2-self.num
        except TypeError as err:
            t = True
        self.assertTrue(t)
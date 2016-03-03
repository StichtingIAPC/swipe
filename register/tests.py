from django.test import TestCase
from register.models import *
from money.models import *

# Create your tests here.

class BasicTest(TestCase):

    def setUp(self):
        self.eu=CurrencyData("EUR","Euro",2,"€")
        self.reg1 = Register(currency=self.eu,is_cash_register=True)
        self.reg2 = Register(currency=self.eu,is_cash_register=False)
        self.denom1 = Denomination(currency=self.eu,amount=2.20371)
        self.denom2 = Denomination(currency=self.eu,amount=2)
        self.denom3 = Denomination(currency=self.eu,amount=0.02)

    def test_register_init(self):
        reg = Register(currency=self.eu,is_cash_register=False)

    def test_get_denoms(self):
        self.eu.save()
        self.reg1.save()
        self.denom1.save()
        self.denom2.save()
        self.denom3.save()
        print(Denomination.objects.all())
        if(self.reg1.is_cash_register):
            a=self.reg1.get_denominations()
            assert(len(a) == 3)

    def test_zdatabase(self):
        a=Denomination.objects.all()
        print(a)




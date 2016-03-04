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
        if(self.reg1.is_cash_register):
            a=self.reg1.get_denominations()
            assert(len(a) == 3)

    def test_checking_sales_periods(self):
        assert (not RegisterManager.get_open_sales_period())
        s = SalesPeriod()
        s.save()
        assert (RegisterManager.get_open_sales_period())

    def test_open_registers(self):
        assert(RegisterManager.number_of_open_registers() == 0)
        sales_period = SalesPeriod()
        sales_period.save()
        self.reg1.save()
        assert(RegisterManager.number_of_open_registers() == 0)
        assert (len(RegisterManager.get_open_registers()) == 0)
        assert(not self.reg1.is_open())
        self.reg1.open()
        assert(self.reg1.is_open())
        assert(RegisterManager.number_of_open_registers() == 1)
        val = False
        try:
            self.reg1.open()
        except AlreadyOpenError:
            val = True
        assert val
        k = RegisterManager.get_open_registers()
        assert (len(RegisterManager.get_open_registers()) == 1)


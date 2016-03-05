from django.test import TestCase
from register.models import *
from money.models import *

# Create your tests here.


class BasicTest(TestCase):

    def setUp(self):
        self.eu = CurrencyData("EUR", "Euro", 2, "€")
        self.usd = CurrencyData("USD", "United States Dollar", 2, "$")
        self.reg1 = Register.create(currency=self.eu, is_cash_register=True, payment_method="Bloop")
        self.reg2 = Register.create(currency=self.eu, is_cash_register=False, payment_method="Foo")
        self.reg3 = Register.create(currency=self.usd, is_cash_register=False, payment_method="Foo")
        self.denom1 = Denomination(currency=self.eu, amount=2.20371)
        self.denom2 = Denomination(currency=self.eu, amount=2)
        self.denom3 = Denomination(currency=self.eu, amount=0.02)

    def test_register_init(self):
        reg = Register(currency=self.eu, is_cash_register=False)
        assert reg

    def test_get_denoms(self):
        self.eu.save()
        self.reg1.save()
        self.denom1.save()
        self.denom2.save()
        self.denom3.save()
        if self.reg1.is_cash_register:
            a = self.reg1.get_denominations()
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
        assert (len(RegisterManager.get_open_registers()) == 1)

    def test_empty_database(self):
        ConsistencyChecker.full_check()
        assert (RegisterManager.number_of_open_registers() == 0)
        assert (not RegisterManager.sales_period_is_open())

    def test_open_multiple_registers(self):
        ConsistencyChecker.full_check()
        assert (RegisterManager.number_of_open_registers() == 0)
        assert (not RegisterManager.sales_period_is_open())
        self.reg1.save()
        self.reg1.open()
        assert (RegisterManager.sales_period_is_open())
        assert (RegisterManager.number_of_open_registers() == 1)
        self.reg2.save()
        self.reg2.open()
        assert (RegisterManager.sales_period_is_open())
        assert (RegisterManager.number_of_open_registers() == 2)
        SalesPeriod.close()
        assert (RegisterManager.number_of_open_registers() == 0)
        assert (not RegisterManager.sales_period_is_open())
        ConsistencyChecker.full_check()

    def test_mult_currency_registers(self):
        ConsistencyChecker.full_check()
        assert (RegisterManager.number_of_open_registers() == 0)
        assert (not RegisterManager.sales_period_is_open())
        self.reg1.save()
        self.reg1.open()
        assert (RegisterManager.sales_period_is_open())
        assert (RegisterManager.number_of_open_registers() == 1)
        self.reg3.save()
        self.reg3.open()
        assert (RegisterManager.sales_period_is_open())
        assert (RegisterManager.number_of_open_registers() == 2)
        ConsistencyChecker.full_check()

    def test_payment_fixing(self):
        self.reg1.save()
        assert self.reg1.payment_method == "Cash"

    def test_payment_methods(self):
        assert (RegisterManager.number_of_open_registers() == 0)
        assert (not RegisterManager.sales_period_is_open())
        self.reg1.save()
        self.reg2.save()
        self.reg3.save()
        payment_types = RegisterManager.get_payment_types_for_open_registers()
        assert len(payment_types) == 0
        self.reg1.open()
        payment_types = RegisterManager.get_payment_types_for_open_registers()
        assert len(payment_types) == 1
        self.reg2.open()
        payment_types = RegisterManager.get_payment_types_for_open_registers()
        assert len(payment_types) == 2
        self.reg3.open()
        payment_types = RegisterManager.get_payment_types_for_open_registers()
        assert len(payment_types) == 2
        ConsistencyChecker.full_check()





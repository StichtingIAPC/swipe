from django.test import TestCase
from register.models import *
from money.models import *

# Create your tests here.


class BasicTest(TestCase):

    def setUp(self):
        self.cash = PaymentType(name="Cash")
        self.pin = PaymentType(name="PIN")
        self.cash.save()
        self.pin.save()
        self.eu = CurrencyData(iso="EUR", name="Euro", digits=2, symbol="€")
        self.usd = CurrencyData(iso="USD", name="United States Dollar", digits=2, symbol="$")
        self.reg1 = Register(currency=self.eu, is_cash_register=True, payment_type=self.cash)
        self.reg2 = Register(currency=self.eu, is_cash_register=False, payment_type=self.pin)
        self.reg3 = Register(currency=self.usd, is_cash_register=False, payment_type=self.pin)
        self.denom1 = Denomination.create(currency=self.eu, amount=2.20371)
        self.denom2 = Denomination.create(currency=self.eu, amount=2)
        self.denom3 = Denomination.create(currency=self.eu, amount=0.02)

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
        assert (not RegisterMaster.get_open_sales_period())
        s = SalesPeriod()
        s.save()
        assert (RegisterMaster.get_open_sales_period())

    def test_open_registers(self):
        assert(RegisterMaster.number_of_open_registers() == 0)
        sales_period = SalesPeriod()
        sales_period.save()
        self.reg1.save()
        assert(RegisterMaster.number_of_open_registers() == 0)
        assert (len(RegisterMaster.get_open_registers()) == 0)
        assert(not self.reg1.is_open())
        self.reg1.open()
        assert(self.reg1.is_open())
        assert(RegisterMaster.number_of_open_registers() == 1)
        val = False
        try:
            self.reg1.open()
        except AlreadyOpenError:
            val = True
        assert val
        assert (len(RegisterMaster.get_open_registers()) == 1)

    def test_empty_database(self):
        ConsistencyChecker.full_check()
        assert (RegisterMaster.number_of_open_registers() == 0)
        assert (not RegisterMaster.sales_period_is_open())

    def test_open_multiple_registers(self):
        ConsistencyChecker.full_check()
        assert (RegisterMaster.number_of_open_registers() == 0)
        assert (not RegisterMaster.sales_period_is_open())
        self.reg1.save()
        self.reg1.open()
        assert (RegisterMaster.sales_period_is_open())
        assert (RegisterMaster.number_of_open_registers() == 1)
        self.reg2.save()
        self.reg2.open()
        assert (RegisterMaster.sales_period_is_open())
        assert (RegisterMaster.number_of_open_registers() == 2)
        SalesPeriod.close()
        assert (RegisterMaster.number_of_open_registers() == 0)
        assert (not RegisterMaster.sales_period_is_open())
        ConsistencyChecker.full_check()

    def test_mult_currency_registers(self):
        ConsistencyChecker.full_check()
        assert (RegisterMaster.number_of_open_registers() == 0)
        assert (not RegisterMaster.sales_period_is_open())
        self.reg1.save()
        self.reg1.open()
        assert (RegisterMaster.sales_period_is_open())
        assert (RegisterMaster.number_of_open_registers() == 1)
        self.reg3.save()
        self.reg3.open()
        assert (RegisterMaster.sales_period_is_open())
        assert (RegisterMaster.number_of_open_registers() == 2)
        ConsistencyChecker.full_check()

    def test_illegal_payment_type(self):
        a = Register(currency=self.eu, is_cash_register=False, payment_type=self.pin)
        a.save()
        b = Register(currency=self.eu, is_cash_register=True, payment_type=self.pin)
        foo = False
        try:
            b.save()
        except AssertionError:
            foo = True
        assert foo

    def test_payment_types(self):
        assert (RegisterMaster.number_of_open_registers() == 0)
        assert (not RegisterMaster.sales_period_is_open())
        self.reg1.save()
        self.reg2.save()
        self.reg3.save()
        payment_types = RegisterMaster.get_payment_types_for_open_registers()
        assert len(payment_types) == 0
        self.reg1.open()
        payment_types = RegisterMaster.get_payment_types_for_open_registers()
        assert len(payment_types) == 1
        self.reg2.open()
        payment_types = RegisterMaster.get_payment_types_for_open_registers()
        assert len(payment_types) == 2
        self.reg3.open()
        payment_types = RegisterMaster.get_payment_types_for_open_registers()
        assert len(payment_types) == 2
        ConsistencyChecker.full_check()


class TestTransaction(TestCase):
    def test_simple(self):
        EUR = Currency("EUR")
        cost = Cost(Decimal("1.21000"), EUR)

        money = Money(Decimal("1.21000"), EUR)
        vat = VAT.objects.create(vatrate=Decimal("1.21"), name="HIGH", active=True)
        price = Price(Decimal("1.21000"), EUR, vat=vat.vatrate)
        art = ArticleType.objects.create(name="P1", vat=vat)
        st = SalesTransactionLine(article=art, count=1, cost=cost, price = price, num=1)
        sp = SalesPeriod.objects.create()
        pay = Payment(salesperiod=sp, amount=money)
        Transaction.construct([pay], [st])
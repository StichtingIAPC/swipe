from django.test import TestCase

from register.models import *
from money.models import *
from stock.exceptions import StockSmallerThanZeroError


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
        self.denom1 = Denomination(currency=self.eu, amount=Decimal("2.20371"))
        self.denom1.save()
        self.denom2 = Denomination(currency=self.eu, amount=Decimal("2.00000"))
        self.denom2.save()
        self.denom3 = Denomination(currency=self.eu, amount=Decimal("0.02000"))
        self.denom3.save()

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
            assert (len(a) == 3)

    def test_checking_sales_periods(self):
        assert (not RegisterMaster.get_open_sales_period())
        s = SalesPeriod()
        s.save()
        assert (RegisterMaster.get_open_sales_period())

    def test_open_registers(self):
        self.eu.save()
        assert (RegisterMaster.number_of_open_registers() == 0)
        sales_period = SalesPeriod()
        sales_period.save()
        self.reg1.save()
        assert (RegisterMaster.number_of_open_registers() == 0)
        assert (len(RegisterMaster.get_open_registers()) == 0)
        assert (not self.reg1.is_open())
        c1 = DenominationCount(denomination=self.denom1, amount=1)
        c2 = DenominationCount(denomination=self.denom2, amount=1)
        c3 = DenominationCount(denomination=self.denom3, amount=1)
        denom_counts = [c1, c2, c3]
        self.reg1.open(Decimal("4.22371"), denominations=denom_counts)
        assert (self.reg1.is_open())
        assert (RegisterMaster.number_of_open_registers() == 1)
        val = False
        try:
            self.reg1.open(Decimal("1.21"))
        except AlreadyOpenError:
            val = True
        assert val
        assert (len(RegisterMaster.get_open_registers()) == 1)

    def test_empty_database(self):
        ConsistencyChecker.full_check()
        assert (RegisterMaster.number_of_open_registers() == 0)
        assert (not RegisterMaster.sales_period_is_open())

    def test_open_multiple_registers(self):
        self.eu.save()
        ConsistencyChecker.full_check()
        assert (RegisterMaster.number_of_open_registers() == 0)
        assert (not RegisterMaster.sales_period_is_open())
        self.reg1.save()
        c1 = DenominationCount(denomination=self.denom1, amount=1)
        c2 = DenominationCount(denomination=self.denom2, amount=1)
        c3 = DenominationCount(denomination=self.denom3, amount=1)
        denom_counts = [c1, c2, c3]
        self.reg1.open(Decimal("4.22371"), denominations=denom_counts)
        assert (RegisterMaster.sales_period_is_open())
        assert (RegisterMaster.number_of_open_registers() == 1)
        self.reg2.save()
        self.reg2.open(Decimal("1.21"))
        assert (RegisterMaster.sales_period_is_open())
        assert (RegisterMaster.number_of_open_registers() == 2)
        reg_count_1 = RegisterCount()
        reg_count_1.register_period = self.reg1.get_current_open_register_period()
        reg_count_1.amount = Decimal("4.22371")
        reg_count_2 = RegisterCount()
        reg_count_2.register_period = self.reg2.get_current_open_register_period()
        reg_count_2.amount = Decimal("10.22371")
        reg_counts = [reg_count_1, reg_count_2]
        c1 = DenominationCount(register_count=reg_count_1, denomination=self.denom1, amount=1)
        c2 = DenominationCount(register_count=reg_count_1, denomination=self.denom2, amount=1)
        c3 = DenominationCount(register_count=reg_count_1, denomination=self.denom3, amount=1)
        denom_counts = [c1, c2, c3]
        trans = OtherTransactionLine(count=1, price=Price(Decimal("1.00000"), self.eu, vat=Decimal("1.21")), num=1,
                                     text="HOI")
        pay = Payment(amount=Money(Decimal("1.00000"), self.eu), payment_type=self.cash)
        MoneyInOut.objects.create(register_period=self.reg1.get_current_open_register_period(),
                                  amount=Decimal("1.0000"))
        Transaction.construct([pay], [trans])

        SalesPeriod.close(registercounts=reg_counts, denominationcounts=denom_counts, memo="HELLO")
        assert (RegisterMaster.number_of_open_registers() == 0)
        assert (not RegisterMaster.sales_period_is_open())
        ConsistencyChecker.full_check()

    def test_mult_open_close(self):
        self.eu.save()
        self.reg1.save()
        c1 = DenominationCount(denomination=self.denom1, amount=1)
        c2 = DenominationCount(denomination=self.denom2, amount=1)
        c3 = DenominationCount(denomination=self.denom3, amount=1)
        denom_counts = [c1, c2, c3]
        self.reg1.open(Decimal("4.22371"), denominations=denom_counts)
        reg_count_1 = RegisterCount()
        reg_count_1.register_period = self.reg1.get_current_open_register_period()
        reg_count_1.amount = Decimal("4.22371")
        reg_counts = [reg_count_1]
        c1 = DenominationCount(register_count=reg_count_1, denomination=self.denom1, amount=1)
        c2 = DenominationCount(register_count=reg_count_1, denomination=self.denom2, amount=1)
        c3 = DenominationCount(register_count=reg_count_1, denomination=self.denom3, amount=1)
        denom_counts = [c1, c2, c3]
        SalesPeriod.close(registercounts=reg_counts, denominationcounts=denom_counts, memo="HELLO")
        c1 = DenominationCount(denomination=self.denom1, amount=1)
        c2 = DenominationCount(denomination=self.denom2, amount=1)
        c3 = DenominationCount(denomination=self.denom3, amount=2)
        denom_counts = [c1, c2, c3]
        self.reg1.open(Decimal("4.24371"), denominations=denom_counts)
        self.assertEqual(len(OpeningCountDifference.objects.all()), 2)
        Money(Decimal("0.02000"), self.eu)

    def test_mult_currency_registers(self):
        self.eu.save()
        ConsistencyChecker.full_check()
        assert (RegisterMaster.number_of_open_registers() == 0)
        assert (not RegisterMaster.sales_period_is_open())
        self.reg1.save()

        c1 = DenominationCount(denomination=self.denom1, amount=1)
        c2 = DenominationCount(denomination=self.denom2, amount=1)
        c3 = DenominationCount(denomination=self.denom3, amount=1)
        denom_counts = [c1, c2, c3]
        self.reg1.open(Decimal("4.22371"), denominations=denom_counts)
        assert (RegisterMaster.sales_period_is_open())
        assert (RegisterMaster.number_of_open_registers() == 1)
        self.reg3.save()
        self.reg3.open(Decimal("1.21"))
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
        self.eu.save()
        assert (RegisterMaster.number_of_open_registers() == 0)
        assert (not RegisterMaster.sales_period_is_open())
        self.reg1.save()
        self.reg2.save()
        self.reg3.save()
        payment_types = RegisterMaster.get_payment_types_for_open_registers()
        assert len(payment_types) == 0
        self.reg1.open(Decimal("4.22371"), denominations=[DenominationCount(denomination=self.denom1, amount=1),
                                                          DenominationCount(denomination=self.denom2, amount=1),
                                                          DenominationCount(denomination=self.denom3, amount=1)])
        payment_types = RegisterMaster.get_payment_types_for_open_registers()
        assert len(payment_types) == 1
        self.reg2.open(Decimal("1.21"))
        payment_types = RegisterMaster.get_payment_types_for_open_registers()
        assert len(payment_types) == 2
        self.reg3.open(Decimal("1.21"))
        payment_types = RegisterMaster.get_payment_types_for_open_registers()
        assert len(payment_types) == 2
        ConsistencyChecker.full_check()


class TestTransactionNoSalesPeriod(TestCase):
    def setUp(self):
        self.EUR = Currency("EUR")
        self.cost = Cost(Decimal("1.21000"), self.EUR)
        self.money = Money(Decimal("1.21000"), self.EUR)
        self.pt = PaymentType.objects.create()
        self.vat = VAT.objects.create(vatrate=Decimal("1.21"), name="HIGH", active=True)
        self.price = Price(Decimal("1.21000"), self.EUR, vat=self.vat.vatrate)
        self.art = ArticleType.objects.create(name="P1", vat=self.vat)

        self.simplest = SalesTransactionLine(article=self.art, count=1, cost=self.cost, price=self.price, num=1)
        self.simple_payment = Payment(amount=self.money, payment_type=self.pt)

    def do_transaction(self):
        Transaction.construct([self.simple_payment], [self.simplest])

    def test_simple(self):
        SalesTransactionLine(article=self.art, count=1, cost=self.cost, price=self.price, num=1)
        Payment(amount=self.money)
        StockChangeSet.construct("HENK", [{
            'article': self.art,
            'book_value': self.cost,
            'count': 1,
            'is_in': True,
        }], 1)
        self.assertRaises(InactiveError, self.do_transaction)
        self.assertEqual(1, StockChange.objects.all().__len__())
        self.assertEqual(0, Payment.objects.all().__len__())


class TestTransaction(TestCase):
    def setUp(self):
        self.EUR = Currency("EUR")
        self.cost = Cost(Decimal("1.21000"), self.EUR)
        self.money = Money(Decimal("1.21000"), self.EUR)
        self.pt = PaymentType.objects.create()
        self.vat = VAT.objects.create(vatrate=Decimal("1.21"), name="HIGH", active=True)
        self.price = Price(Decimal("1.21000"), self.EUR, vat=self.vat.vatrate)
        self.art = ArticleType.objects.create(name="P1", vat=self.vat)
        self.sp = SalesPeriod.objects.create()
        self.simplest = SalesTransactionLine(article=self.art, count=1, cost=self.cost, price=self.price, num=1)
        self.simple_payment = Payment(amount=self.money, payment_type=self.pt)

    def do_transaction(self):
        Transaction.construct([self.simple_payment], [self.simplest])

    def test_simple(self):
        SalesTransactionLine(article=self.art, count=1, cost=self.cost, price=self.price, num=1)
        Payment(amount=self.money)
        StockChangeSet.construct("HENK", [{
            'article': self.art,
            'book_value': self.cost,
            'count': 1,
            'is_in': True,
        }], 1)
        self.do_transaction()
        self.assertEqual(2, StockChange.objects.all().__len__())
        self.assertEqual(1, Payment.objects.all().__len__())

    def test_fail_no_stock(self):
        SalesTransactionLine(article=self.art, count=1, cost=self.cost, price=self.price, num=1)
        Payment(amount=self.money, payment_type=self.pt)
        self.assertRaises(StockSmallerThanZeroError, self.do_transaction)
        self.assertEqual(0, StockChange.objects.all().__len__())
        self.assertEqual(0, Payment.objects.all().__len__())

    def test_fail_no_consistent_pay(self):
        self.simple_payment = Payment(amount=self.money * 2)
        StockChangeSet.construct("HENK", [{
            'article': self.art,
            'book_value': self.cost,
            'count': 1,
            'is_in': True,
        }], 1)
        # A payment with different amount of Payment than products should FAIL
        self.assertRaises(AssertionError, self.do_transaction)
        self.assertEqual(1, StockChange.objects.all().__len__())
        self.assertEqual(0, Payment.objects.all().__len__())

from decimal import Decimal

from django.test import TestCase

from crm.models import User
from money.models import CurrencyData, Denomination, Price, Money, AccountingGroup, VAT, Currency
from register import models
from register.models import PaymentType, Register, RegisterMaster, SalesPeriod, DenominationCount, AlreadyOpenError, \
    ConsistencyChecker, RegisterCount, MoneyInOut, OpeningCountDifference, ClosingCountDifference
from sales.models import Payment, OtherTransactionLine, Transaction
from tools.testing import TestData


class BasicTest(TestCase, TestData):
    def setUp(self):
        self.part_setup_currency_data()
        self.cash = PaymentType(name="Cash")
        self.pin = PaymentType(name="PIN")
        self.cash.save()
        self.pin.save()
        self.eu = CurrencyData(iso="EUR", name="Euro", digits=2, symbol="€")
        self.usd = CurrencyData(iso="USD", name="United States Dollar", digits=2, symbol="$")
        self.reg1 = Register(currency=self.currency_data_used, is_cash_register=True, payment_type=self.cash, name="A")
        self.reg2 = Register(currency=self.currency_data_used, is_cash_register=False, payment_type=self.pin, name='B')
        self.reg3 = Register(currency=self.usd, is_cash_register=False, payment_type=self.pin, name='C')
        self.denom1 = Denomination(currency=self.currency_data_used, amount=Decimal("2.20371"))
        self.denom1.save()
        self.denom2 = Denomination(currency=self.currency_data_used, amount=Decimal("2.00000"))
        self.denom2.save()
        self.denom3 = Denomination(currency=self.currency_data_used, amount=Decimal("0.02000"))
        self.denom3.save()
        self.copro = User()
        self.copro.save()

        self.vat_group = VAT()
        self.vat_group.name = "AccGrpFoo"
        self.vat_group.active = True
        self.vat_group.vatrate = 1.12
        self.vat_group.save()
        self.price = Price(amount=Decimal("1.00"), use_system_currency=True)
        self.currency = Currency(iso="EUR")

        self.acc_group = AccountingGroup()
        self.acc_group.accounting_number = 2
        self.acc_group.vat_group = self.vat_group
        self.acc_group.save()

    def test_register_init(self):
        reg = Register(currency=self.eu, is_cash_register=False)
        self.assertTrue(not not reg)

    def test_get_denoms(self):
        self.eu.save()
        self.reg1.save()
        self.denom1.save()
        self.denom2.save()
        self.denom3.save()
        if self.reg1.is_cash_register:
            a = self.reg1.get_denominations()
            self.assertEquals(len(a), 3)

    def test_checking_sales_periods(self):
        self.assertFalse(RegisterMaster.get_open_sales_period())
        s = SalesPeriod()
        s.save()
        self.assertTrue(RegisterMaster.get_open_sales_period())

    def test_open_registers(self):
        self.eu.save()
        self.assertEquals(RegisterMaster.number_of_open_registers(), 0)
        sales_period = SalesPeriod()
        sales_period.save()
        self.reg1.save()
        self.assertEquals(RegisterMaster.number_of_open_registers(), 0)
        self.assertEquals(len(RegisterMaster.get_open_registers()), 0)
        self.assertFalse(self.reg1.is_open())
        c1 = DenominationCount(denomination=self.denom1, number=1)
        c2 = DenominationCount(denomination=self.denom2, number=1)
        c3 = DenominationCount(denomination=self.denom3, number=1)
        denom_counts = [c1, c2, c3]
        self.reg1.open(Decimal("4.22371"), denominations=denom_counts)
        self.assertTrue(self.reg1.is_open())
        self.assertEquals(RegisterMaster.number_of_open_registers(), 1)
        counting_difference = OpeningCountDifference.objects.get()
        self.assertEqual(counting_difference.difference, Money(amount=Decimal("4.22371"), currency=Currency(self.eu.iso)))

        with self.assertRaises(AlreadyOpenError):
            self.reg1.open(Decimal("1.21"))

        self.assertEquals(len(RegisterMaster.get_open_registers()), 1)

    def test_empty_database(self):
        ConsistencyChecker.full_check()
        self.assertEquals(RegisterMaster.number_of_open_registers(), 0)
        self.assertFalse(RegisterMaster.sales_period_is_open())

    def test_open_multiple_registers(self):
        self.eu.save()
        ConsistencyChecker.full_check()
        self.assertEquals(RegisterMaster.number_of_open_registers(), 0)
        self.assertFalse(RegisterMaster.sales_period_is_open())
        self.reg1.save()
        c1 = DenominationCount(denomination=self.denom1, number=1)
        c2 = DenominationCount(denomination=self.denom2, number=1)
        c3 = DenominationCount(denomination=self.denom3, number=1)
        denom_counts = [c1, c2, c3]
        self.reg1.open(Decimal("4.22371"), denominations=denom_counts)
        self.assertTrue(RegisterMaster.sales_period_is_open())
        self.assertEquals(RegisterMaster.number_of_open_registers(), 1)
        self.reg2.save()
        self.reg2.open(Decimal("1.21"))
        self.assertTrue(RegisterMaster.sales_period_is_open())
        self.assertEquals(RegisterMaster.number_of_open_registers(), 2)
        reg_count_1 = RegisterCount()
        reg_count_1.register_period = self.reg1.get_current_open_register_period()
        reg_count_1.amount = Decimal("4.22371")
        reg_count_2 = RegisterCount()
        reg_count_2.register_period = self.reg2.get_current_open_register_period()
        reg_count_2.amount = Decimal("10.22371")
        reg_counts = [reg_count_1, reg_count_2]
        c1 = DenominationCount(register_count=reg_count_1, denomination=self.denom1, number=1)
        c2 = DenominationCount(register_count=reg_count_1, denomination=self.denom2, number=1)
        c3 = DenominationCount(register_count=reg_count_1, denomination=self.denom3, number=1)
        denom_counts = [c1, c2, c3]
        trans = OtherTransactionLine(count=1, price=Price(Decimal("1.00000"), vat=Decimal("1.21"), currency=Currency(self.currency_data_used.iso)),
                                     num=1, text="HOI", user_modified=self.copro, accounting_group=self.acc_group)
        pay = Payment(amount=Money(Decimal("1.00000"), self.currency_data_used.as_currency()), payment_type=self.cash)
        MoneyInOut.objects.create(register_period=self.reg1.get_current_open_register_period(),
                                  amount=Decimal("1.0000"))
        Transaction.create_transaction(user=self.copro, payments=[pay], transaction_lines=[trans])

        SalesPeriod.close(registercounts=reg_counts, denominationcounts=denom_counts, memo="HELLO")
        self.assertEquals(RegisterMaster.number_of_open_registers(), 0)
        self.assertFalse(RegisterMaster.sales_period_is_open())
        ConsistencyChecker.full_check()

    def test_mult_open_close(self):
        self.reg1.save()
        c1 = DenominationCount(denomination=self.denom1, number=1)
        c2 = DenominationCount(denomination=self.denom2, number=1)
        c3 = DenominationCount(denomination=self.denom3, number=1)
        denom_counts = [c1, c2, c3]
        self.reg1.open(Decimal("4.22371"), denominations=denom_counts)
        reg_count_1 = RegisterCount()
        reg_count_1.register_period = self.reg1.get_current_open_register_period()
        reg_count_1.amount = Decimal("4.22371")
        reg_counts = [reg_count_1]
        c1 = DenominationCount(register_count=reg_count_1, denomination=self.denom1, number=1)
        c2 = DenominationCount(register_count=reg_count_1, denomination=self.denom2, number=1)
        c3 = DenominationCount(register_count=reg_count_1, denomination=self.denom3, number=1)
        denom_counts = [c1, c2, c3]
        SalesPeriod.close(registercounts=reg_counts, denominationcounts=denom_counts, memo="HELLO")
        c1 = DenominationCount(denomination=self.denom1, number=1)
        c2 = DenominationCount(denomination=self.denom2, number=1)
        c3 = DenominationCount(denomination=self.denom3, number=2)
        denom_counts = [c1, c2, c3]
        self.reg1.open(Decimal("4.24371"), denominations=denom_counts)
        self.assertEqual(len(OpeningCountDifference.objects.all()), 2)

    def test_mult_currency_registers(self):
        self.eu.save()
        ConsistencyChecker.full_check()
        self.assertEquals(RegisterMaster.number_of_open_registers(), 0)
        self.assertFalse(RegisterMaster.sales_period_is_open())
        self.reg1.save()

        c1 = DenominationCount(denomination=self.denom1, number=1)
        c2 = DenominationCount(denomination=self.denom2, number=1)
        c3 = DenominationCount(denomination=self.denom3, number=1)
        denom_counts = [c1, c2, c3]
        self.reg1.open(Decimal("4.22371"), denominations=denom_counts)
        self.assertTrue(RegisterMaster.sales_period_is_open())
        self.assertEquals(RegisterMaster.number_of_open_registers(), 1)
        self.reg3.save()
        self.reg3.open(Decimal("1.21"))
        self.assertTrue(RegisterMaster.sales_period_is_open())
        self.assertEquals(RegisterMaster.number_of_open_registers(), 2)
        ConsistencyChecker.full_check()

    def test_illegal_payment_type(self):
        a = Register(currency=self.eu, is_cash_register=False, payment_type=self.pin)
        a.save()
        b = Register(currency=self.eu, is_cash_register=True, payment_type=self.pin)

        with self.assertRaises(models.CurrencyTypeMismatchError):
            b.save()

    def test_payment_types(self):
        self.eu.save()
        self.assertEquals(RegisterMaster.number_of_open_registers(), 0)
        self.assertFalse(RegisterMaster.sales_period_is_open())
        self.reg1.save()
        self.reg2.save()
        self.reg3.save()
        payment_types = RegisterMaster.get_payment_types_for_open_registers()
        self.assertEquals(len(payment_types), 0)
        self.reg1.open(Decimal("4.22371"), denominations=[DenominationCount(denomination=self.denom1, number=1),
                                                          DenominationCount(denomination=self.denom2, number=1),
                                                          DenominationCount(denomination=self.denom3, number=1)])
        payment_types = RegisterMaster.get_payment_types_for_open_registers()
        self.assertEquals(len(payment_types), 1)
        self.reg2.open(Decimal("1.21"))
        payment_types = RegisterMaster.get_payment_types_for_open_registers()
        self.assertEquals(len(payment_types), 2)
        self.reg3.open(Decimal("1.21"))
        payment_types = RegisterMaster.get_payment_types_for_open_registers()
        self.assertEquals(len(payment_types), 2)
        ConsistencyChecker.full_check()

    def test_opening_no_count_difference(self):
        self.eu.save()
        sales_period = SalesPeriod()
        sales_period.save()
        self.reg1.save()
        # Open for the first time
        c1 = DenominationCount(denomination=self.denom1, number=0)
        c2 = DenominationCount(denomination=self.denom2, number=0)
        c3 = DenominationCount(denomination=self.denom3, number=0)
        denom_counts = [c1, c2, c3]
        self.reg1.open(Decimal("0"), denominations=denom_counts)
        counting_difference = OpeningCountDifference.objects.get()
        self.assertEqual(counting_difference.difference, Money(amount=Decimal("0"), currency=Currency(self.eu.iso)))

        current_register_period=self.reg1.get_current_open_register_period()
        money_in = MoneyInOut(amount=Decimal("2"), register_period=current_register_period)
        money_in.save()

        reg_count_1 = RegisterCount()
        reg_count_1.register_period = current_register_period
        reg_count_1.amount = Decimal("2")
        reg_counts = [reg_count_1]
        c1 = DenominationCount(register_count=reg_count_1, denomination=self.denom1, number=0)
        c2 = DenominationCount(register_count=reg_count_1, denomination=self.denom2, number=1)
        c3 = DenominationCount(register_count=reg_count_1, denomination=self.denom3, number=0)
        denom_counts = [c1, c2, c3]
        SalesPeriod.close(registercounts=reg_counts, denominationcounts=denom_counts, memo="")
        counting_difference = ClosingCountDifference.objects.get()
        self.assertEqual(counting_difference.difference, Money(amount=Decimal("0"), currency=Currency(self.eu.iso)))

        c1 = DenominationCount(denomination=self.denom1, number=0)
        c2 = DenominationCount(denomination=self.denom2, number=1)
        c3 = DenominationCount(denomination=self.denom3, number=0)
        denom_counts = [c1, c2, c3]
        self.reg1.open(Decimal("2"), denominations=denom_counts)
        counting_difference=OpeningCountDifference.objects.all().last()
        self.assertEqual(counting_difference.difference, Money(amount=Decimal("0"), currency=Currency(self.eu.iso)))

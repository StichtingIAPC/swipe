from _pydecimal import Decimal

from mockdatagen.helpers import MockGen
from money.models import CurrencyData, Denomination
from register.models import PaymentType, Register, RegisterCount, SalesPeriod, DenominationCount, RegisterMaster


@MockGen.register
class PaymentTypeGen:
    model = PaymentType

    @staticmethod
    def func():
        PaymentType.objects.get_or_create(name="Maestro", is_invoicing=False)
        PaymentType.objects.get_or_create(name="Cash", is_invoicing=False)
        PaymentType.objects.get_or_create(name="Invoice", is_invoicing=True)

    requirements = {}


@MockGen.register
class RegisterGen:
    model = Register

    @staticmethod
    def func():
        cur = CurrencyData.objects.get(iso="EUR")
        mae = PaymentType.objects.get(name="Maestro")
        cas = PaymentType.objects.get(name="Cash")
        inv = PaymentType.objects.get(name="Invoice")
        Register.objects.get_or_create(name="Maestro Register", currency=cur, payment_type=mae)
        Register.objects.get_or_create(name="Cash Register", currency=cur, is_cash_register=True, payment_type=cas)
        Register.objects.get_or_create(name="Invoice Register", currency=cur, payment_type=inv)

    requirements = {PaymentType, CurrencyData}


@MockGen.register
class RegisterOpenClose:
    model = "PRE"

    @staticmethod
    def func():
        mae = Register.objects.get(name="Maestro Register")
        cash = Register.objects.get(name="Cash Register")
        mae.open(Decimal(0))
        cash.open(Decimal(0))
        SalesPeriod.close([(RegisterCount(register=mae, amount=Decimal(10)), None), (
            RegisterCount(register=cash, amount=Decimal(10)),
            [DenominationCount(denomination=Denomination.objects.get(amount=Decimal(2)), number=5)])])

    requirements = {Register}


@MockGen.register
class IncoiceOpen:
    model = "invoiceOpen"

    @staticmethod
    def func():
        inv = Register.objects.get(name="Invoice Register")
        inv.open(Decimal(0))

    requirements = {"PRE"}
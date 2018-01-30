from _pydecimal import Decimal
from datetime import datetime

from mockdatagen.helpers import MockGen
from money.models import CurrencyData, Denomination, VAT, VATPeriod, AccountingGroup


@MockGen.register
class CurrencyDataGen:
    model = CurrencyData

    @staticmethod
    def func():
        CurrencyData.objects.get_or_create(iso="EUR", name="Euro", symbol="€", digits=2)

    requirements = {}


@MockGen.register
class DenominationDataGen:
    model = Denomination

    @staticmethod
    def func():
        cur = CurrencyData.objects.first()
        Denomination.objects.get_or_create(currency=cur, amount=Decimal(0.05))
        Denomination.objects.get_or_create(currency=cur, amount=Decimal(0.1))
        Denomination.objects.get_or_create(currency=cur, amount=Decimal(0.2))
        Denomination.objects.get_or_create(currency=cur, amount=Decimal(0.5))
        Denomination.objects.get_or_create(currency=cur, amount=Decimal(1))
        Denomination.objects.get_or_create(currency=cur, amount=Decimal(2))
        Denomination.objects.get_or_create(currency=cur, amount=Decimal(5))
        Denomination.objects.get_or_create(currency=cur, amount=Decimal(10))
        Denomination.objects.get_or_create(currency=cur, amount=Decimal(20))
        Denomination.objects.get_or_create(currency=cur, amount=Decimal(50))
        Denomination.objects.get_or_create(currency=cur, amount=Decimal(100))
        Denomination.objects.get_or_create(currency=cur, amount=Decimal(200))
        Denomination.objects.get_or_create(currency=cur, amount=Decimal(500))

    requirements = {CurrencyData}


@MockGen.register
class VatDataGen:
    model = VAT

    @staticmethod
    def func():
        VAT.objects.get_or_create(name="HIGH", active=True)
        VAT.objects.get_or_create(name="LOW", active=True)

    requirements = {}


@MockGen.register
class VatPeriodDataGen:
    model = VATPeriod

    @staticmethod
    def func():
        vat = VAT.objects.get(name="LOW")
        vat2 = VAT.objects.get(name="HIGH")
        time = datetime(2010, 6, 18, 21, 18, 22, 449637)
        VATPeriod.objects.get_or_create(vat=vat, begin_date=time, vatrate=Decimal(1.06))
        VATPeriod.objects.get_or_create(vat=vat2, begin_date=time, vatrate=Decimal(1.21))

    requirements = {VAT}


@MockGen.register
class AccountingGroupGen:
    model = AccountingGroup

    @staticmethod
    def func():
        vat = VAT.objects.get(name="LOW")
        vat2 = VAT.objects.get(name="HIGH")
        time = datetime(2010, 6, 18, 21, 18, 22, 449637)
        AccountingGroup.objects.get_or_create(vat_group=vat2, accounting_number=1921, name="Other")
        AccountingGroup.objects.get_or_create(vat_group=vat, accounting_number=1337, name="Books")

    requirements = {VAT}

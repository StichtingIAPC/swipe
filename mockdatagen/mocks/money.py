from _pydecimal import Decimal
from datetime import datetime

from mockdatagen.models import register
from money.models import CurrencyData, Denomination, VAT, VATPeriod


class CurrencyDataGen:
    model = CurrencyData

    def func(self):
        CurrencyData.objects.get_or_create(iso="EUR", name="Euro", symbol="€", digits=2)
        print(CurrencyData.objects.all())


    requirements = {}


register(CurrencyDataGen)


class DenominationDataGen:
    model = Denomination

    def func(self):
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
        print(Denomination.objects.all())

    requirements = {CurrencyData}


register(DenominationDataGen)


class VatDataGen:
    model = VAT

    def func(self):
        VAT.objects.get_or_create(name="HIGH", active=True)
        VAT.objects.get_or_create(name="LOW", active=True)
        print(VAT.objects.all())

    requirements = {}


register(VatDataGen)


class VatPeriodDataGen:
    model = VATPeriod

    def func(self):
        vat = VAT.objects.get(name="LOW")
        vat2 = VAT.objects.get(name="HIGH")
        time = datetime(2010, 6, 18, 21, 18, 22, 449637)
        VATPeriod.objects.get_or_create(vat=vat, begin_date=time, vatrate=Decimal(1.06))
        VATPeriod.objects.get_or_create(vat=vat2, begin_date=time, vatrate=Decimal(1.21))
        print(VATPeriod.objects.all())

    requirements = {VAT}


register(VatPeriodDataGen)

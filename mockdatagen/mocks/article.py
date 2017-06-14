from _pydecimal import Decimal
from datetime import datetime

from article.models import ArticleType
from assortment.models import AssortmentUnitType, AssortmentLabelType, AssortmentLabel
from mockdatagen.helpers import register
from money.models import CurrencyData, Denomination, VAT, VATPeriod, AccountingGroup


@register
class LabelUnitTypeGen:
    model = AssortmentLabel

    @staticmethod
    def func():
        AssortmentUnitType.objects.all().delete()
        AssortmentLabelType.objects.all().delete()

        countable_int_type_hertz = AssortmentUnitType.objects.create(
            type_short='Hz',  # Hz is just an example of integer values.
            type_long='hertz',  #
            value_type='i',  # i for integer
            incremental_type='SI'  # SI counting for this unittype
        )
        number_type_meter = AssortmentUnitType.objects.create(
            type_short='m',  # meter
            type_long='meter',  #
            value_type='n',  # n for number
            incremental_type='SI'  # SI counting for this unittype

        )
        AssortmentLabelType.objects.create(
            description='Length',
            name='length',
            unit_type=number_type_meter
        )
        AssortmentLabelType.objects.create(
            description='CPU cycles per second',
            name='clock speed',
            unit_type=countable_int_type_hertz
        )

    requirements = {}


@register
class ArticleTypeGen:
    model = ArticleType

    @staticmethod
    def func():
        other = AccountingGroup.objects.get(name="Other")
        books = AccountingGroup.objects.get(name="Books")
        ArticleType.objects.get_or_create(name="Micro Usb Cable", accounting_group=other, ean=1234567890123)
        ArticleType.objects.get_or_create(name="Geen Probleem", accounting_group=books, ean=1234567890124)

    requirements = {AccountingGroup}
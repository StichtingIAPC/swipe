from _pydecimal import Decimal

from article.models import ArticleType
from assortment.models import AssortmentUnitType, AssortmentLabelType, AssortmentLabel
from mockdatagen.helpers import MockGen
from mockdatagen.mocks.article import ArticleTypeGen
from money.models import AccountingGroup, Cost, Currency
from stock.models import StockChangeSet


@MockGen.register
class StockGen:
    model = StockChangeSet

    @staticmethod
    def func():
        art = ArticleType.objects.get(name="Geen Probleem")
        cur = Currency("EUR")

        sp = Cost(amount=Decimal("2.00000"), currency=cur)

        # Construct entry list for StockChangeSet
        entries = [{
            'article': art,
            'book_value': sp,
            'count': 2,
            'is_in': True
        }]

        StockChangeSet.construct("Pro forma", entries, StockChangeSet.SOURCE_TEST_DO_NOT_USE)

    requirements = {ArticleType}

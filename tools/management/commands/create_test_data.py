from decimal import Decimal
from django.core.management.base import BaseCommand

# Creates Test data
from article.models import ArticleType
from assortment.models import AssortmentArticleBranch
from money.models import CurrencyData, Denomination, VAT, AccountingGroup, Currency, Cost
from register.models import PaymentType
from register.models import Register
from stock.models import StockChangeSet


class Command(BaseCommand):
    def handle(self, *args, **options):
        eur = CurrencyData.objects.create(iso="EUR", symbol="€",name="EURO", digits=2)
        Denomination.objects.create(currency=eur, amount=0.01)
        Denomination.objects.create(currency=eur, amount=0.02)
        Denomination.objects.create(currency=eur, amount=0.05)
        Denomination.objects.create(currency=eur, amount=0.1)
        Denomination.objects.create(currency=eur, amount=0.2)
        Denomination.objects.create(currency=eur, amount=0.5)
        Denomination.objects.create(currency=eur, amount=1)
        Denomination.objects.create(currency=eur, amount=2)
        Denomination.objects.create(currency=eur, amount=5)
        Denomination.objects.create(currency=eur, amount=10)
        Denomination.objects.create(currency=eur, amount=20)
        Denomination.objects.create(currency=eur, amount=50)
        Denomination.objects.create(currency=eur, amount=100)
        Denomination.objects.create(currency=eur, amount=200)
        Denomination.objects.create(currency=eur, amount=500)
        cash = PaymentType.objects.create(name="Cash")
        maestro = PaymentType.objects.create(name="Maestro")
        invoice = PaymentType.objects.create(name="Invoice")
        bitcoin = PaymentType.objects.create(name="Bitcoin")
        Register.objects.create(name="Cash", currency=eur, is_cash_register=True, is_active=True, payment_type=cash)
        Register.objects.create(name="Maestro", currency=eur, is_cash_register=False, is_active=True, payment_type=maestro)
        Register.objects.create(name="Invoice", currency=eur, is_cash_register=False, is_active=True, payment_type=invoice)
        Register.objects.create(name="Bitcoin", currency=eur, is_cash_register=False, is_active=False, payment_type=bitcoin)
        high = VAT.objects.create(name="high", active=True, vatrate=1.21)
        low  = VAT.objects.create(name="high", active=True, vatrate=1.06)
        stock_group = AccountingGroup.objects.create(accounting_number=8840, vat_group=high)
        book_group = AccountingGroup.objects.create(accounting_number=3927, vat_group=low)
        branch = AssortmentArticleBranch.objects.create(
            name='hoi',
            parent_tag=None)


        cur = Currency("EUR")
        print(cur.iso)

        art1 = ArticleType.objects.create(branch=branch, accounting_group=stock_group, name="Bomb")
        art2 = ArticleType.objects.create(branch=branch, accounting_group=book_group, name="How to cook fries")
        sp = Cost(amount=Decimal("2.00000"), currency=cur)
        # Construct entry list for StockChangeSet

        entries = [{
            'article': art1,
            'book_value': sp,
            'count': 2,
            'is_in': True
        }]
        StockChangeSet.construct(description="AddToStockTest1", entries=entries, enum=1)
        sp = Cost(amount=Decimal("4.00000"), currency=cur)
        # Construct entry list for StockChangeSet
        entries = [{
            'article': art2,
            'book_value': sp,
            'count': 2,
            'is_in': True
        }]
        # Execute two stock modifications, creating two StockLogs

        StockChangeSet.construct(description="AddToStockTest2", entries=entries, enum=1)
from decimal import Decimal
from django.core.management.base import BaseCommand

# Creates Test data
from article.models import ArticleType
from assortment.models import AssortmentArticleBranch
from money.models import CurrencyData, Denomination, VAT, AccountingGroup, Currency, Cost
from register.models import PaymentType
from register.models import Register
from stock.models import StockChangeSet
from money.models import Price
from order.models import Order
from crm.models import Person, User
from logistics.models import SupplierOrder
from supplier.models import Supplier, ArticleTypeSupplier
from supplication.models import PackingDocument


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

        user_1 = User(username="jsteen")
        user_1.save()

        user_2 = User(username="astaartjes")
        user_2.save()

        customer_1 = Person.objects.create(address="Drienerlolaan 5", city="Enschede", email="bestuur@iapc.utwente.nl",
                                        name="Jaap de Steen", phone="0534893927", zip_code="7522NB")
        customer_2 = Person.objects.create(address="Drienerlolaan 5", city="Enschede", email="schaduwbestuur@iapc.utwente.nl",
                                           name="Gerda Steenhuizen", phone="0534894260", zip_code="7522NB")

        supplier_1 = Supplier.objects.create(name="Copaco")

        supplier_2 = Supplier.objects.create(name="McDos")

        cost_1 = Cost(amount=Decimal(0.74), use_system_currency=True)

        cost_2 = Cost(amount=Decimal(0.85), use_system_currency=True)

        cost_3 = Cost(amount=Decimal(0.23), use_system_currency=True)

        cost_4 = Cost(amount=Decimal(2.37), use_system_currency=True)

        ats_1 = ArticleTypeSupplier(article_type=art1, supplier=supplier_1,
                                  cost=cost_1, minimum_number_to_order=1, supplier_string="At1", availability='A')
        ats_1.save()

        ats2 = ArticleTypeSupplier(supplier=supplier_1, article_type=art2,
                                   cost=cost_2, minimum_number_to_order=1, supplier_string="At2", availability='A')
        ats2.save()

        ats_3 = ArticleTypeSupplier(article_type=art1, supplier=supplier_2,
                                  cost=cost_3, minimum_number_to_order=1, supplier_string="FD1", availability='A')
        ats_3.save()

        ats_4 = ArticleTypeSupplier(article_type=art2, supplier=supplier_2,
                                    cost=cost_4, minimum_number_to_order=1, supplier_string="FD2", availability='A')
        ats_4.save()

        price_1 = Price(amount=Decimal(1.11), use_system_currency=True)
        price_2 = Price(amount=Decimal(2.23), use_system_currency=True)

        Order.create_order_from_wishables_combinations(customer=customer_1,
                                                       wishable_type_number_price_combinations=[[art1, 5, price_1],
                                                                                                [art2, 7, price_2]],
                                                       user=user_1)

        Order.create_order_from_wishables_combinations(customer=customer_2,
                                                       wishable_type_number_price_combinations=[[art1, 11, price_1],
                                                                                                [art2, 13, price_2]],
                                                       user=user_2)

        SupplierOrder.create_supplier_order(user_modified=user_1, supplier=supplier_1, articles_ordered=[[art1, 7, cost_1],
                                                                                                         [art2, 5, cost_2]])

        SupplierOrder.create_supplier_order(user_modified=user_2, supplier=supplier_2,
                                            articles_ordered=[[art1, 3, cost_3],
                                                              [art2, 4, cost_4]])

        PackingDocument.create_packing_document(user=user_1, supplier=supplier_1, packing_document_name="0118999",
                                                article_type_cost_combinations=[[art1, 4], [art2, 3]])

        PackingDocument.create_packing_document(user=user_2, supplier=supplier_2, packing_document_name="|--|<<<",
                                                article_type_cost_combinations=[[art1, 2], [art2, 3]])

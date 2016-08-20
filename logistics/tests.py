from django.test import TestCase
from money.models import VAT, Price, Currency, AccountingGroup, Money
from article.models import ArticleType
from crm.models import User, Person
from logistics.models import *
from order.models import *
from unittest import skip
from decimal import Decimal


class StockWishTests(TestCase):

    def setUp(self):
        self.vat_group = VAT()
        self.vat_group.name = "AccGrpFoo"
        self.vat_group.active = True
        self.vat_group.vatrate = 1.12
        self.vat_group.save()
        self.price = Price(amount=Decimal("1.00"), use_system_currency=True)
        self.currency = Currency(iso="USD")

        self.acc_group = AccountingGroup()
        self.acc_group.accounting_number = 2
        self.acc_group.vat_group = self.vat_group
        self.acc_group.save()

        self.article_type = ArticleType(accounting_group=self.acc_group, name="Foo1")
        self.article_type.save()

        self.at2 = ArticleType(accounting_group=self.acc_group, name="Foo2")
        self.at2.save()

        self.at3 = ArticleType(accounting_group=self.acc_group, name="Foo3")
        self.at3.save()

        self.money = Money(amount=Decimal(3.32), currency=self.currency)

        self.customer = Person()
        self.customer.save()

        self.copro = User()
        self.copro.save()

    def test_primitive_wish_save(self):
        NUMBER = 2
        sw = StockWish.create_stock_wish(
            user=self.copro,
            articles_ordered=[
                (self.article_type, NUMBER)
            ])

        assert len(StockWish.objects.all()) == 1
        swtl = StockWishTableLog.objects.get()
        assert swtl.stock_wish == sw

        swtl = StockWishTableLine.objects.all()
        assert len(swtl) == 1
        assert swtl[0].article_type == self.article_type
        assert swtl[0].number == NUMBER

    def test_addition_wish(self):
        NUMBER = 1
        NUMBER2 = 2
        NUMBER3 = -1

        stock_wish = StockWish.create_stock_wish(
            user=self.copro,
            articles_ordered=[
                (self.article_type, NUMBER),
                (self.article_type, NUMBER2)
            ]
        )

        StockWish.create_stock_wish(
            user=self.copro,
            articles_ordered=[
                (self.article_type, NUMBER3)
            ]
        )

        swtl = StockWishTableLine.objects.all()
        assert len(swtl) == 1
        assert swtl[0].number == NUMBER + NUMBER2 + NUMBER3

        logs = StockWishTableLog.objects.all()
        assert len(logs) == 3

        assert logs[0].supplier_order is None and logs[0].stock_wish == stock_wish

    def test_differentiation_wish(self):
        NUMBER = 2
        NUMBER2 = 3

        sw = StockWish.create_stock_wish(
            user=self.copro,
            articles_ordered=[
                (self.article_type, NUMBER),
                (self.at2, NUMBER2)
            ]
        )

        swtls = StockWishTableLine.objects.all()
        assert len(swtls) == 2

        for swtl in swtls:
            if swtl.article_type == self.article_type:
                assert swtl.number == NUMBER
            elif swtl.article_type == self.at2:
                assert swtl.number == NUMBER2

        assert len(StockWishTableLog.objects.all()) == 2

    def test_mass_storage_simple(self):

        article_number_list = []
        article_number_list.append([self.article_type, 2])
        StockWish.create_stock_wish(self.copro, article_number_list)

        stockwish_list = StockWish.objects.all()
        assert len(stockwish_list) == 1
        assert stockwish_list[0].copro == self.copro

        logs = StockWishTableLog.objects.all()
        assert len(logs) == 1

        assert logs[0].stock_wish == stockwish_list[0]

    def test_mass_storage_compound(self):

        article_number_list = [
            (self.article_type, 2),
            (self.article_type, 2)
        ]
        StockWish.create_stock_wish(self.copro, article_number_list)

        stockwish_list = StockWish.objects.all()
        assert len(stockwish_list) == 1
        assert stockwish_list[0].copro == self.copro

        logs = StockWishTableLog.objects.all()
        assert len(logs) == 2

        assert logs[0].stock_wish == stockwish_list[0]
        assert logs[1].stock_wish == stockwish_list[0]

        stock_wish_table_lines = StockWishTableLine.objects.all()
        assert len(stock_wish_table_lines) == 1

    def test_mass_storage_differentiated(self):

        atcs = []
        atcs.append([self.article_type, 2])
        atcs.append([self.article_type, 2])
        atcs.append([self.at2, 3])
        atcs.append([self.at3, 5])
        StockWish.create_stock_wish(self.copro, atcs)

        stockwish_list = StockWish.objects.all()
        assert len(stockwish_list) == 1
        assert stockwish_list[0].copro == self.copro

        logs = StockWishTableLog.objects.all()
        assert len(logs) == 4

        stock_wish_table_lines = StockWishTableLine.objects.all()
        assert len(stock_wish_table_lines) == 3

    def test_indirection(self):

        log = StockWishTableLog(number=3, article_type=self.article_type)
        caught = False
        try:
            log.save()
        except IndirectionError:
            caught = True
        assert caught


class SupplierOrderTests(TestCase):

    def setUp(self):
        self.vat_group = VAT()
        self.vat_group.name = "AccGrpFoo"
        self.vat_group.active = True
        self.vat_group.vatrate = 1.12
        self.vat_group.save()
        self.price = Price(amount=Decimal("1.00"), use_system_currency=True)
        self.currency = Currency(iso="USD")

        self.acc_group = AccountingGroup()
        self.acc_group.accounting_number = 2
        self.acc_group.vat_group = self.vat_group
        self.acc_group.save()

        self.article_type = ArticleType(accounting_group=self.acc_group, name="Foo1")
        self.article_type.save()

        self.at2 = ArticleType(accounting_group=self.acc_group, name="Foo2")
        self.at2.save()

        self.at3 = ArticleType(accounting_group=self.acc_group, name="Foo3")
        self.at3.save()

        self.money = Money(amount=Decimal(3.32), currency=self.currency)

        self.customer = Person()
        self.customer.save()

        self.copro = User()
        self.copro.save()

        self.supplier = Supplier(name="Nepacove")
        self.supplier.save()

    def test_ics_strategy_orders_only(self):
        orderlines = []
        DEMAND_1=6
        DEMAND_2=3
        OrderLine.add_orderlines_to_list(orderlines, self.at2, DEMAND_2, self.price, self.copro)
        OrderLine.add_orderlines_to_list(orderlines, self.article_type, DEMAND_1, self.price, self.copro)
        order = Order(copro=self.copro, customer=self.customer)
        Order.make_order(order, orderlines)
        atcs = []
        SUP_ORD_1 = 2
        SUP_ORD_2 = 3
        atcs.append((self.article_type, SUP_ORD_1))
        atcs.append((self.at2, SUP_ORD_2))
        assert SUP_ORD_1 <= DEMAND_1
        assert SUP_ORD_2 <= DEMAND_2
        # We know supply <= demand

        dist = IndiscriminateCustomerStockStrategy.get_distribution(atcs)
        article_type_count = defaultdict(lambda: 0)
        for d in dist:
            article_type_count[d.article_type] += 1

        for atc in article_type_count:
            if atc == self.article_type:
                assert article_type_count[atc] == SUP_ORD_1
            else:
                assert article_type_count[atc] == SUP_ORD_2

    def test_ics_strategy_stock_only(self):
        atcs = []
        DEMAND_1 = 6
        DEMAND_2 = 3
        atcs.append((self.article_type, DEMAND_1))
        atcs.append((self.at2, DEMAND_2))
        StockWish.create_stock_wish(user=self.copro, articles_ordered=atcs)

    @skip("Not finished")
    def test_new_function(self):
        # Articletypes for supplier order
        atcs = []
        atcs.append((self.article_type, 2))
        atcs.append((self.article_type, 2))
        atcs.append((self.at2, 2))
        atcs.append((self.article_type, 2))

        # Orders
        orderlines = []
        OrderLine.add_orderlines_to_list(orderlines, self.at2, 3, self.price, self.copro)
        OrderLine.add_orderlines_to_list(orderlines, self.article_type, 6, self.price, self.copro)
        order = Order(copro=self.copro, customer=self.customer)
        Order.make_order(order, orderlines)
        #SupplierOrder.create_supplier_order(user=self.copro, supplier=self.supplier, articles_ordered=atcs)




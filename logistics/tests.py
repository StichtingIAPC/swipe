from django.test import TestCase
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

    def test_deletion_of_lines(self):
        atcs = []
        atcs.append([self.article_type, 2])
        StockWish.create_stock_wish(self.copro, atcs)
        assert len(StockWishTableLog.objects.all()) == 1
        swtl = StockWishTableLine.objects.all()
        assert len(swtl) == 1
        assert swtl[0].number == 2


        atcs = []
        atcs.append([self.article_type, -1])
        StockWish.create_stock_wish(self.copro, atcs)
        assert len(StockWishTableLog.objects.all()) == 2
        swtl = StockWishTableLine.objects.all()
        assert len(swtl) == 1
        assert swtl[0].number == 1


        atcs = []
        atcs.append([self.article_type, -1])
        StockWish.create_stock_wish(self.copro, atcs)
        assert len(StockWishTableLog.objects.all()) == 3
        swtl = StockWishTableLine.objects.all()
        assert len(swtl) == 0

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

        cost = Cost(amount=Decimal(1), use_system_currency=True)

        self.supplier = Supplier(name="Nepacove")
        self.supplier.save()

        ats = ArticleTypeSupplier(article_type=self.article_type, supplier=self.supplier,
                                  cost=cost, minimum_number_to_order=1, supplier_string="At1", availability='A')
        ats.save()
        ats2 = ArticleTypeSupplier(supplier=self.supplier, article_type=self.at2,
                                   cost=cost, minimum_number_to_order=1, supplier_string="At2", availability='A')
        ats2.save()
        self.money = Money(amount=Decimal(3.32), currency=self.currency)

        self.customer = Person()
        self.customer.save()

        self.copro = User()
        self.copro.save()

    def test_ics_strategy_orders_only(self):
        orderlines = []
        DEMAND_1=6
        DEMAND_2=3
        OrderLine.add_orderlines_to_list(orderlines, self.article_type, DEMAND_1, self.price, self.copro)
        OrderLine.add_orderlines_to_list(orderlines, self.at2, DEMAND_2, self.price, self.copro)
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
            assert d.order_line is not None

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

        atcs = []
        SUPPLY_1 = 2
        SUPPLY_2 = 3
        atcs.append((self.article_type, SUPPLY_1))
        atcs.append((self.at2, SUPPLY_2))

        distribution = IndiscriminateCustomerStockStrategy.get_distribution(article_type_number_combos=atcs)
        count = defaultdict(lambda: 0)
        for d in distribution:
            count[d.article_type] += 1
            assert d.order_line is None
        assert (count[self.article_type]) == SUPPLY_1
        assert (count[self.at2]) == SUPPLY_2

    def test_ics_strategy_combined(self):
        STOCK_DEMAND_1 = 2
        STOCK_DEMAND_2 = 2

        ORDER_DEMAND_1 = 2
        ORDER_DEMAND_2 = 2
        atcs = []
        atcs.append((self.article_type, STOCK_DEMAND_1))
        atcs.append((self.at2, STOCK_DEMAND_2))
        StockWish.create_stock_wish(user=self.copro, articles_ordered=atcs)

        orderlines = []

        OrderLine.add_orderlines_to_list(orderlines, self.article_type, ORDER_DEMAND_1, self.price, self.copro)
        OrderLine.add_orderlines_to_list(orderlines, self.at2, ORDER_DEMAND_2, self.price, self.copro)
        order = Order(copro=self.copro, customer=self.customer)
        Order.make_order(order, orderlines)

        SUPPLY_1 = 3
        SUPPLY_2 = 3

        atcs = []
        atcs.append((self.article_type, SUPPLY_1))
        atcs.append((self.at2, SUPPLY_2))
        distribution = IndiscriminateCustomerStockStrategy.get_distribution(atcs)
        counted_orders = 0
        for d in distribution:
            if d.order_line is not None:
                counted_orders += 1
        assert counted_orders == ORDER_DEMAND_1 + ORDER_DEMAND_2

    def test_distribution_to_orders(self):
        # Articletypes for supplier order
        ORDER_1 = 6
        ORDER_2 = 3

        SUPPLY_1 = 5
        SUPPLY_2 = 3

        atcs = []
        atcs.append((self.article_type, SUPPLY_1))
        atcs.append((self.at2, SUPPLY_2))

        ats = ArticleTypeSupplier(supplier=self.supplier, article_type=self.article_type)
        # Orders
        orderlines = []
        OrderLine.add_orderlines_to_list(orderlines, self.article_type, ORDER_1, self.price, self.copro)
        OrderLine.add_orderlines_to_list(orderlines, self.at2, ORDER_2, self.price, self.copro)

        order = Order(copro=self.copro, customer=self.customer)
        Order.make_order(order, orderlines)

        SupplierOrder.create_supplier_order(user=self.copro, supplier=self.supplier, articles_ordered=atcs)
        sols = SupplierOrderLine.objects.all()

        FOUND_1 = 0
        FOUND_2 = 0
        for sol in sols:
            assert sol.supplier_order.supplier == self.supplier
            assert sol.supplier_order.copro == self.copro
            if sol.article_type == self.article_type:
                FOUND_1 += 1
            if sol.article_type == self.at2:
                FOUND_2 += 1
        assert FOUND_1 == SUPPLY_1
        assert FOUND_2 == SUPPLY_2

    def test_distribution_to_stock(self):

        STOCK_1 = 6
        STOCK_2 = 3

        atcs = []
        atcs.append((self.article_type, STOCK_1))
        atcs.append((self.at2, STOCK_2))

        StockWish.create_stock_wish(user=self.copro, articles_ordered=atcs)


        SUPPLY_1 = 5
        SUPPLY_2 = 3

        atcs = []
        atcs.append((self.article_type, SUPPLY_1))
        atcs.append((self.at2, SUPPLY_2))

        SupplierOrder.create_supplier_order(user=self.copro, supplier=self.supplier, articles_ordered=atcs)

        sols = SupplierOrderLine.objects.all()

        FOUND_1 = 0
        FOUND_2 = 0

        for sol in sols:
            assert sol.order_line is None
            if sol.article_type == self.article_type:
                FOUND_1 += 1
            if sol.article_type == self.at2:
                FOUND_2 += 1

        assert SUPPLY_1 == FOUND_1
        assert SUPPLY_2 == FOUND_2

    def test_distribution_mixed(self):

        STOCK_DEMAND_1 = 2
        STOCK_DEMAND_2 = 2

        ORDER_DEMAND_1 = 2
        ORDER_DEMAND_2 = 2
        atcs = []
        atcs.append((self.article_type, STOCK_DEMAND_1))
        atcs.append((self.at2, STOCK_DEMAND_2))
        StockWish.create_stock_wish(user=self.copro, articles_ordered=atcs)

        orderlines = []

        OrderLine.add_orderlines_to_list(orderlines, self.article_type, ORDER_DEMAND_1, self.price, self.copro)
        OrderLine.add_orderlines_to_list(orderlines, self.at2, ORDER_DEMAND_2, self.price, self.copro)
        order = Order(copro=self.copro, customer=self.customer)
        Order.make_order(order, orderlines)

        SUPPLY_1 = 3
        SUPPLY_2 = 3

        atcs = []
        atcs.append((self.article_type, SUPPLY_1))
        atcs.append((self.at2, SUPPLY_2))

        SupplierOrder.create_supplier_order(user=self.copro, supplier=self.supplier, articles_ordered=atcs)
        sols = SupplierOrderLine.objects.all()

        ORDERS = 0

        for sol in sols:
            if sol.order_line is not None:
                ORDERS += 1
        assert ORDERS == ORDER_DEMAND_1+ORDER_DEMAND_2





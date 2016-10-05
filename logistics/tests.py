from django.test import TestCase

from article.tests import INeedSettings
from logistics.models import *
from order.models import *


class StockWishTests(INeedSettings, TestCase):

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

        super().setUp()

        self.article_type = ArticleType(accounting_group=self.acc_group,
                                        name="Foo1", branch=self.branch)
        self.article_type.save()

        self.at2 = ArticleType(accounting_group=self.acc_group,
                               name="Foo2", branch=self.branch)
        self.at2.save()

        self.at3 = ArticleType(accounting_group=self.acc_group, name="Foo3",
                               branch=self.branch)
        self.at3.save()

        self.money = Money(amount=Decimal(3.32), currency=self.currency)

        self.customer = Person()
        self.customer.save()

        self.user_modified = User(username= "HENK")
        self.user_modified.save()

    def test_primitive_wish_save(self):
        NUMBER = 2
        sw = StockWish.create_stock_wish(
            user_modified=self.user_modified,
            articles_ordered=[
                (self.article_type, NUMBER)
            ])

        self.assertEqual(len(StockWish.objects.all()), 1)
        swtl = StockWishTableLog.objects.get()
        self.assertEquals(swtl.stock_wish , sw)

        swtl = StockWishTableLine.objects.all()
        self.assertEquals(len(swtl) , 1)
        self.assertEquals(swtl[0].article_type , self.article_type)
        self.assertEquals(swtl[0].number , NUMBER)

    def test_addition_wish(self):
        NUMBER = 1
        NUMBER2 = 2
        NUMBER3 = -1

        stock_wish = StockWish.create_stock_wish(
            user_modified=self.user_modified,
            articles_ordered=[
                (self.article_type, NUMBER),
                (self.article_type, NUMBER2)
            ]
        )

        StockWish.create_stock_wish(
            user_modified=self.user_modified,
            articles_ordered=[
                (self.article_type, NUMBER3)
            ]
        )

        swtl = StockWishTableLine.objects.all()
        self.assertEqual(len(swtl), 1)
        self.assertEqual(swtl[0].number, NUMBER + NUMBER2 + NUMBER3)

        logs = StockWishTableLog.objects.all()
        self.assertEqual(len(logs), 3)

        self.assertIsNone(logs[0].supplier_order)
        self.assertEqual(logs[0].stock_wish, stock_wish)

    def test_differentiation_wish(self):
        NUMBER = 2
        NUMBER2 = 3

        sw = StockWish.create_stock_wish(
            user_modified=self.user_modified,
            articles_ordered=[
                (self.article_type, NUMBER),
                (self.at2, NUMBER2)
            ]
        )

        swtls = StockWishTableLine.objects.all()
        self.assertEqual(len(swtls), 2)

        for swtl in swtls:
            if swtl.article_type == self.article_type:
                self.assertEqual(swtl.number, NUMBER)
            elif swtl.article_type == self.at2:
                self.assertEqual(swtl.number, NUMBER2)

        self.assertEqual(len(StockWishTableLog.objects.all()), 2)

    def test_mass_storage_simple(self):

        article_number_list = []
        article_number_list.append([self.article_type, 2])
        StockWish.create_stock_wish(self.user_modified, article_number_list)

        stockwish_list = StockWish.objects.all()
        self.assertEqual(len(stockwish_list), 1)
        self.assertEqual(stockwish_list[0].user_created, self.user_modified)

        logs = StockWishTableLog.objects.all()
        self.assertEqual(len(logs), 1)

        self.assertEqual(logs[0].stock_wish, stockwish_list[0])

    def test_mass_storage_compound(self):

        article_number_list = [
            (self.article_type, 2),
            (self.article_type, 2)
        ]
        StockWish.create_stock_wish(self.user_modified, article_number_list)

        stockwish_list = StockWish.objects.all()
        self.assertEqual(len(stockwish_list), 1)
        self.assertEqual(stockwish_list[0].user_created, self.user_modified)

        logs = StockWishTableLog.objects.all()
        self.assertEqual(len(logs), 2)

        self.assertEqual(logs[0].stock_wish, stockwish_list[0])
        self.assertEqual(logs[1].stock_wish, stockwish_list[0])

        stock_wish_table_lines = StockWishTableLine.objects.all()
        self.assertEqual(len(stock_wish_table_lines), 1)

    def test_mass_storage_differentiated(self):

        atcs = []
        atcs.append([self.article_type, 2])
        atcs.append([self.article_type, 2])
        atcs.append([self.at2, 3])
        atcs.append([self.at3, 5])
        StockWish.create_stock_wish(self.user_modified, atcs)

        stockwish_list = StockWish.objects.all()
        self.assertEqual(len(stockwish_list), 1)
        self.assertEqual(stockwish_list[0].user_created, self.user_modified)

        logs = StockWishTableLog.objects.all()
        self.assertEqual(len(logs), 4)

        stock_wish_table_lines = StockWishTableLine.objects.all()
        self.assertEqual(len(stock_wish_table_lines), 3)

    def test_deletion_of_lines(self):
        atcs = []
        atcs.append([self.article_type, 2])
        StockWish.create_stock_wish(self.user_modified, atcs)
        self.assertEqual(len(StockWishTableLog.objects.all()), 1)
        swtl = StockWishTableLine.objects.all()
        self.assertEqual(len(swtl), 1)
        self.assertEqual(swtl[0].number, 2)


        atcs = []
        atcs.append([self.article_type, -1])
        StockWish.create_stock_wish(self.user_modified, atcs)
        self.assertEqual(len(StockWishTableLog.objects.all()), 2)
        swtl = StockWishTableLine.objects.all()
        self.assertEqual(len(swtl), 1)
        self.assertEqual(swtl[0].number, 1)


        atcs = []
        atcs.append([self.article_type, -1])
        StockWish.create_stock_wish(self.user_modified, atcs)
        self.assertEqual(len(StockWishTableLog.objects.all()), 3)
        swtl = StockWishTableLine.objects.all()
        self.assertEqual(len(swtl), 0)

    def test_indirection(self):

        log = StockWishTableLog(number=3, article_type=self.article_type,user_modified=self.user_modified)

        with self.assertRaises(IndirectionError):
            log.save()


class SupplierOrderTests(INeedSettings, TestCase):

    def setUp(self):
        self.vat_group = VAT()
        self.vat_group.name = "AccGrpFoo"
        self.vat_group.active = True
        self.vat_group.vatrate = 1.12
        self.vat_group.save()
        self.price = Price(amount=Decimal("1.00"), use_system_currency=True)
        self.currency = Currency(iso="USD")
        super().setUp()

        self.acc_group = AccountingGroup()
        self.acc_group.accounting_number = 2
        self.acc_group.vat_group = self.vat_group
        self.acc_group.save()

        self.article_type = ArticleType(accounting_group=self.acc_group,
                                        name="Foo1", branch=self.branch)
        self.article_type.save()

        self.at2 = ArticleType(accounting_group=self.acc_group,
                               name="Foo2", branch=self.branch)
        self.at2.save()

        self.at3 = ArticleType(accounting_group=self.acc_group,
                               name="Foo3", branch=self.branch)
        self.at3.save()

        cost = Cost(amount=Decimal(1), use_system_currency=True)

        self.supplier = Supplier(name="Nepacove")
        self.supplier.save()

        self.supplier2 = Supplier(name="Bas")
        self.supplier2.save()

        ats = ArticleTypeSupplier(article_type=self.article_type, supplier=self.supplier,
                                  cost=cost, minimum_number_to_order=1, supplier_string="At1", availability='A')
        ats.save()
        ats2 = ArticleTypeSupplier(supplier=self.supplier, article_type=self.at2,
                                   cost=cost, minimum_number_to_order=1, supplier_string="At2", availability='A')
        ats2.save()
        self.money = Money(amount=Decimal(3.32), currency=self.currency)

        self.customer = Person()
        self.customer.save()

        self.user_modified = User()
        self.user_modified.save()

        self.cost = Cost(currency=Currency('EUR'), amount=Decimal(1.23))

    def test_ics_strategy_orders_only(self):
        orderlines = []
        DEMAND_1=6
        DEMAND_2=3
        OrderLine.add_orderlines_to_list(orderlines, self.article_type, DEMAND_1, self.price, self.user_modified)
        OrderLine.add_orderlines_to_list(orderlines, self.at2, DEMAND_2, self.price, self.user_modified)
        order = Order(user_modified=self.user_modified, customer=self.customer)
        Order.make_order(order, orderlines, self.user_modified)
        atcs = []
        SUP_ORD_1 = 2
        SUP_ORD_2 = 3
        atcs.append([self.article_type, SUP_ORD_1, self.cost])
        atcs.append([self.at2, SUP_ORD_2, self.cost])
        self.assertLessEqual(SUP_ORD_1, DEMAND_1)
        self.assertLessEqual(SUP_ORD_2, DEMAND_2)
        # We know supply <= demand

        dist = IndiscriminateCustomerStockStrategy.get_distribution(atcs)
        article_type_count = defaultdict(lambda: 0)
        for d in dist:
            article_type_count[d.article_type] += 1
            self.assertIsNotNone(d.order_line)

        for atc in article_type_count:
            if atc == self.article_type:
                self.assertEqual(article_type_count[atc], SUP_ORD_1)
            else:
                self.assertEqual(article_type_count[atc], SUP_ORD_2)

    def test_ics_strategy_stock_only(self):
        atcs = []
        DEMAND_1 = 6
        DEMAND_2 = 3
        atcs.append((self.article_type, DEMAND_1))
        atcs.append((self.at2, DEMAND_2))
        StockWish.create_stock_wish(user_modified=self.user_modified, articles_ordered=atcs)

        atcs = []
        SUPPLY_1 = 2
        SUPPLY_2 = 3
        atcs.append([self.article_type, SUPPLY_1, self.cost])
        atcs.append([self.at2, SUPPLY_2, self.cost])

        distribution = IndiscriminateCustomerStockStrategy.get_distribution(article_type_number_combos=atcs)
        count = defaultdict(lambda: 0)
        for d in distribution:
            count[d.article_type] += 1
            self.assertIsNone(d.order_line)
        self.assertEqual((count[self.article_type]), SUPPLY_1)
        self.assertEqual((count[self.at2]), SUPPLY_2)

    def test_ics_strategy_combined(self):
        STOCK_DEMAND_1 = 2
        STOCK_DEMAND_2 = 2

        ORDER_DEMAND_1 = 2
        ORDER_DEMAND_2 = 2
        atcs = []
        atcs.append((self.article_type, STOCK_DEMAND_1))
        atcs.append((self.at2, STOCK_DEMAND_2))
        StockWish.create_stock_wish(user_modified=self.user_modified, articles_ordered=atcs)

        orderlines = []

        OrderLine.add_orderlines_to_list(orderlines, self.article_type, ORDER_DEMAND_1, self.price, self.user_modified)
        OrderLine.add_orderlines_to_list(orderlines, self.at2, ORDER_DEMAND_2, self.price, self.user_modified)
        order = Order(user_modified=self.user_modified, customer=self.customer)
        Order.make_order(order, orderlines, self.user_modified)

        SUPPLY_1 = 3
        SUPPLY_2 = 3

        atcs = []
        atcs.append([self.article_type, SUPPLY_1, self.cost])
        atcs.append([self.at2, SUPPLY_2, self.cost])
        distribution = IndiscriminateCustomerStockStrategy.get_distribution(atcs)
        counted_orders = 0
        for d in distribution:
            if d.order_line is not None:
                counted_orders += 1
        self.assertEqual(counted_orders, ORDER_DEMAND_1 + ORDER_DEMAND_2)

    def test_distribution_to_orders(self):
        # Articletypes for supplier order
        ORDER_1 = 6
        ORDER_2 = 3

        SUPPLY_1 = 5
        SUPPLY_2 = 3

        atcs = []
        atcs.append([self.article_type, SUPPLY_1, self.cost])
        atcs.append([self.at2, SUPPLY_2, self.cost])

        ats = ArticleTypeSupplier(supplier=self.supplier, article_type=self.article_type)
        # Orders
        orderlines = []
        OrderLine.add_orderlines_to_list(orderlines, self.article_type, ORDER_1, self.price, self.user_modified)
        OrderLine.add_orderlines_to_list(orderlines, self.at2, ORDER_2, self.price, self.user_modified)

        order = Order(user_modified=self.user_modified, customer=self.customer)
        Order.make_order(order, orderlines, self.user_modified)

        SupplierOrder.create_supplier_order(user_modified=self.user_modified, supplier=self.supplier, articles_ordered=atcs)
        sols = SupplierOrderLine.objects.all()

        FOUND_1 = 0
        FOUND_2 = 0
        for sol in sols:
            self.assertEqual(sol.supplier_order.supplier, self.supplier)
            self.assertEqual(sol.supplier_order.user_created, self.user_modified)
            if sol.article_type == self.article_type:
                FOUND_1 += 1
            if sol.article_type == self.at2:
                FOUND_2 += 1
        self.assertEqual(FOUND_1, SUPPLY_1)
        self.assertEqual(FOUND_2, SUPPLY_2)

    def test_distribution_to_stock(self):

        STOCK_1 = 6
        STOCK_2 = 3

        atcs = []
        atcs.append((self.article_type, STOCK_1))
        atcs.append((self.at2, STOCK_2))

        StockWish.create_stock_wish(user_modified=self.user_modified, articles_ordered=atcs)


        SUPPLY_1 = 5
        SUPPLY_2 = 3

        atcs = []
        atcs.append([self.article_type, SUPPLY_1, self.cost])
        atcs.append([self.at2, SUPPLY_2, self.cost])

        SupplierOrder.create_supplier_order(user_modified=self.user_modified, supplier=self.supplier, articles_ordered=atcs)

        sols = SupplierOrderLine.objects.all()

        FOUND_1 = 0
        FOUND_2 = 0

        for sol in sols:
            self.assertIsNone(sol.order_line)
            if sol.article_type == self.article_type:
                FOUND_1 += 1
            if sol.article_type == self.at2:
                FOUND_2 += 1

        self.assertEqual(SUPPLY_1, FOUND_1)
        self.assertEqual(SUPPLY_2, FOUND_2)

    def test_distribution_mixed(self):

        STOCK_DEMAND_1 = 2
        STOCK_DEMAND_2 = 2

        ORDER_DEMAND_1 = 2
        ORDER_DEMAND_2 = 2
        atcs = []
        atcs.append((self.article_type, STOCK_DEMAND_1))
        atcs.append((self.at2, STOCK_DEMAND_2))
        StockWish.create_stock_wish(user_modified=self.user_modified, articles_ordered=atcs)

        orderlines = []

        OrderLine.add_orderlines_to_list(orderlines, self.article_type, ORDER_DEMAND_1, self.price, self.user_modified)
        OrderLine.add_orderlines_to_list(orderlines, self.at2, ORDER_DEMAND_2, self.price, self.user_modified)
        order = Order(user_modified=self.user_modified, customer=self.customer)
        Order.make_order(order, orderlines, self.user_modified)

        SUPPLY_1 = 3
        SUPPLY_2 = 3

        atcs = []
        atcs.append([self.article_type, SUPPLY_1, self.cost])
        atcs.append([self.at2, SUPPLY_2, self.cost])

        SupplierOrder.create_supplier_order(user_modified=self.user_modified, supplier=self.supplier, articles_ordered=atcs)
        sols = SupplierOrderLine.objects.all()

        ORDERS = 0

        for sol in sols:
            if sol.order_line is not None:
                ORDERS += 1
        self.assertEqual(ORDERS, ORDER_DEMAND_1+ORDER_DEMAND_2)

    def test_cancel_order_with_full_cancel(self):
        ORDER_1 = 1
        orderlines = []
        OrderLine.add_orderlines_to_list(orderlines, self.article_type, ORDER_1, self.price, self.user_modified)
        order = Order(user_modified=self.user_modified, customer=self.customer)
        Order.make_order(order, orderlines, self.user_modified)
        SUPPLY_1 = 1
        atcs = []
        atcs.append([self.article_type, SUPPLY_1, self.cost])
        SupplierOrder.create_supplier_order(user_modified=self.user_modified, supplier=self.supplier,
                                            articles_ordered=atcs)
        ol = OrderLine.objects.get()
        self.assertEqual(ol.state, 'L')
        sol = SupplierOrderLine.objects.get()
        sol.cancel_line(user_modified=self.user_modified, cancel_order=True)
        ol = OrderLine.objects.get()
        self.assertEqual(ol.state, 'C')
        sol = SupplierOrderLine.objects.get()
        self.assertEqual(sol.state, 'C')

    def test_cancel_order_with_return_to_order(self):
        ORDER_1 = 1
        orderlines = []
        OrderLine.add_orderlines_to_list(orderlines, self.article_type, ORDER_1, self.price, self.user_modified)
        order = Order(user_modified=self.user_modified, customer=self.customer)
        Order.make_order(order, orderlines, self.user_modified)
        SUPPLY_1 = 1
        atcs = []
        atcs.append([self.article_type, SUPPLY_1, self.cost])
        SupplierOrder.create_supplier_order(user_modified=self.user_modified, supplier=self.supplier,
                                            articles_ordered=atcs)
        ol = OrderLine.objects.get()
        self.assertEqual(ol.state, 'L')
        sol = SupplierOrderLine.objects.get()
        sol.cancel_line(user_modified=self.user_modified)
        ol = OrderLine.objects.get()
        self.assertEqual(ol.state, 'O')
        sol = SupplierOrderLine.objects.get()
        self.assertEqual(sol.state, 'C')

    def test_cancel_stock_wish_with_full_cancel(self):

        STOCK_DEMAND_1 = 1
        atcs = []
        atcs.append((self.article_type, STOCK_DEMAND_1))
        StockWish.create_stock_wish(user_modified=self.user_modified, articles_ordered=atcs)
        SUPPLY_1 = 1
        atcs = []
        atcs.append([self.article_type, SUPPLY_1, self.cost])
        SupplierOrder.create_supplier_order(user_modified=self.user_modified, supplier=self.supplier,
                                            articles_ordered=atcs)
        stw = StockWishTableLine.objects.all()
        # We removed all the stockwishes from the table
        self.assertEqual(len(stw), 0)
        sol = SupplierOrderLine.objects.get()
        sol.cancel_line(self.user_modified, cancel_order=True)
        self.assertEqual(sol.state, 'C')
        stw = StockWishTableLine.objects.all()
        # All quiet on the stock order front
        self.assertEqual(len(stw), 0)

    def test_cancel_stock_wish_with_return_to_stockwish(self):

        STOCK_DEMAND_1 = 1
        atcs = []
        atcs.append((self.article_type, STOCK_DEMAND_1))
        StockWish.create_stock_wish(user_modified=self.user_modified, articles_ordered=atcs)
        SUPPLY_1 = 1
        atcs = []
        atcs.append([self.article_type, SUPPLY_1, self.cost])
        SupplierOrder.create_supplier_order(user_modified=self.user_modified, supplier=self.supplier,
                                            articles_ordered=atcs)
        stw = StockWishTableLine.objects.all()
        # We removed all the stockwishes from the table
        self.assertEqual(len(stw), 0)
        sol = SupplierOrderLine.objects.get()
        sol.cancel_line(self.user_modified)
        self.assertEqual(sol.state, 'C')
        stw = StockWishTableLine.objects.all()
        # All quiet on the stock order front
        self.assertEqual(len(stw), 1)
        swtls = StockWishTableLog.objects.all()
        # Last modification and return from supplier order
        self.assertEqual(swtls[2].supplier_order, sol.supplier_order)

    def test_supplier_order_combination_line(self):

        STOCK_DEMAND_1 = 2
        STOCK_DEMAND_2 = 2

        ORDER_DEMAND_1 = 2
        ORDER_DEMAND_2 = 2
        atcs = []
        atcs.append((self.article_type, STOCK_DEMAND_1))
        atcs.append((self.at2, STOCK_DEMAND_2))
        StockWish.create_stock_wish(user_modified=self.user_modified, articles_ordered=atcs)

        orderlines = []

        OrderLine.add_orderlines_to_list(orderlines, self.article_type, ORDER_DEMAND_1, self.price, self.user_modified)
        OrderLine.add_orderlines_to_list(orderlines, self.at2, ORDER_DEMAND_2, self.price, self.user_modified)
        order = Order(user_modified=self.user_modified, customer=self.customer)
        Order.make_order(order, orderlines, self.user_modified)

        SUPPLY_1 = 3
        SUPPLY_2 = 3

        atcs = []
        atcs.append([self.article_type, SUPPLY_1, self.cost])
        atcs.append([self.at2, SUPPLY_2, self.cost])

        SupplierOrder.create_supplier_order(user_modified=self.user_modified, supplier=self.supplier, articles_ordered=atcs)
        sols = SupplierOrderLine.objects.all()
        socls = SupplierOrderCombinationLine.get_sol_combinations()
        self.assertEqual(len(socls), 2)
        # If the below broke, the functionality of the system might have changed a bit(especially distribution). It might be OK.
        self.assertEqual(socls[0].number, 3)
        self.assertEqual(socls[1].number, 3)

    def test_supplier_order_combination_line_with_supplier(self):

        STOCK_DEMAND_1 = 2
        atcs = []
        atcs.append((self.article_type, STOCK_DEMAND_1))
        StockWish.create_stock_wish(user_modified=self.user_modified, articles_ordered=atcs)
        SUPPLY_1 = 2
        atcs = []
        atcs.append([self.article_type, SUPPLY_1, self.cost])
        SupplierOrder.create_supplier_order(user_modified=self.user_modified, supplier=self.supplier,
                                            articles_ordered=atcs)
        socls = SupplierOrderCombinationLine.get_sol_combinations(supplier=self.supplier2)
        self.assertEqual(len(socls), 0)
        socls2 = SupplierOrderCombinationLine.get_sol_combinations(supplier=self.supplier)
        self.assertEqual(len(socls2), 1)












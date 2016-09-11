from django.test import TestCase
from decimal import Decimal
from money.models import VAT, AccountingGroup, Price, Currency, Cost, Money
from article.models import ArticleType
from crm.models import Person, User
from supplier.models import Supplier, ArticleTypeSupplier
from logistics.models import SupplierOrder, StockWish
from order.models import OrderLine, Order
from supplication.models import *
from stock.models import Stock
from unittest import skip

# Create your tests here.
class SimpleClassTests(TestCase):

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

        self.cost = Cost(currency=Currency('EUR'), amount=Decimal(1.23))

    def test_simple_book_in_cost_from_supplier_order_line(self):
        order = Order(user_modified=self.copro, customer=self.customer)
        order.save()
        orderlines = []
        OrderLine.add_orderlines_to_list(orderlines, number=1, wishable_type=self.article_type,
                                         price=Price(amount=Decimal(1.55), currency=Currency("EUR")), user=self.copro)
        Order.make_order(order, orderlines, self.copro)
        SupplierOrder.create_supplier_order(user_modified=self.copro, supplier=self.supplier,
                                            articles_ordered=[[self.article_type, 1, self.cost]])
        pac_doc = PackingDocument(supplier=self.supplier, supplier_identifier="Foo", user_modified=self.copro)
        pac_doc.save()
        sol = SupplierOrderLine.objects.get()
        pac_doc_line = PackingDocumentLine(article_type=self.article_type,
                                           packing_document=pac_doc, supplier_order_line=sol, user_modified=self.copro)
        pac_doc_line.save()
        pd = PackingDocumentLine.objects.get()
        assert pd.line_cost == pd.supplier_order_line.line_cost

    def test_simple_book_in_cost_from_invoice(self):
        order = Order(user_modified=self.copro, customer=self.customer)
        order.save()
        orderlines = []
        OrderLine.add_orderlines_to_list(orderlines, number=1, wishable_type=self.article_type,
                                         price=Price(amount=Decimal(1.55), currency=Currency("EUR")), user=self.copro)
        Order.make_order(order, orderlines, self.copro)
        SupplierOrder.create_supplier_order(user_modified=self.copro, supplier=self.supplier,
                                            articles_ordered=[[self.article_type, 1, self.cost]])
        pac_doc = PackingDocument(supplier=self.supplier, supplier_identifier="Foo", user_modified=self.copro)
        pac_doc.save()
        sol = SupplierOrderLine.objects.get()
        inv = Invoice(user_modified=self.copro, supplier=self.supplier)
        inv.save()
        cost = Cost(amount=Decimal(2.78), use_system_currency=True)
        pac_doc_line = PackingDocumentLine(article_type=self.article_type,
                                           packing_document=pac_doc, supplier_order_line=sol,
                                           line_cost_after_invoice=cost, invoice=inv, user_modified=self.copro)
        pac_doc_line.save()
        assert pac_doc_line.invoice == inv
        assert pac_doc_line.line_cost == self.cost
        assert pac_doc_line.line_cost_after_invoice == cost

    def test_illegal_article_type(self):
        order = Order(user_modified=self.copro, customer=self.customer)
        order.save()
        orderlines = []
        OrderLine.add_orderlines_to_list(orderlines, number=1, wishable_type=self.article_type,
                                         price=Price(amount=Decimal(1.55), currency=Currency("EUR")), user=self.copro)
        Order.make_order(order, orderlines, self.copro)
        SupplierOrder.create_supplier_order(user_modified=self.copro, supplier=self.supplier,
                                            articles_ordered=[[self.article_type, 1, self.cost]])
        pac_doc = PackingDocument(supplier=self.supplier, supplier_identifier="Foo", user_modified=self.copro)
        pac_doc.save()
        sol = SupplierOrderLine.objects.get()
        pac_doc_line = PackingDocumentLine(article_type=self.at2,
                                           packing_document=pac_doc, supplier_order_line=sol, user_modified=self.copro)
        caught = False
        try:
            pac_doc_line.save()
        except AssertionError:
            caught = True
        assert caught

    def test_invoice_without_associated_line_cost(self):
        order = Order(user_modified=self.copro, customer=self.customer)
        order.save()
        orderlines = []
        OrderLine.add_orderlines_to_list(orderlines, number=1, wishable_type=self.article_type,
                                         price=Price(amount=Decimal(1.55), currency=Currency("EUR")), user=self.copro)
        Order.make_order(order, orderlines, self.copro)
        SupplierOrder.create_supplier_order(user_modified=self.copro, supplier=self.supplier,
                                            articles_ordered=[[self.article_type, 1, self.cost]])
        pac_doc = PackingDocument(supplier=self.supplier, supplier_identifier="Foo", user_modified=self.copro)
        pac_doc.save()
        sol = SupplierOrderLine.objects.get()
        inv = Invoice(user_modified=self.copro, supplier=self.supplier)
        inv.save()
        cost = Cost(amount=Decimal(2.78), use_system_currency=True)
        pac_doc_line = PackingDocumentLine(article_type=self.article_type,
                                           packing_document=pac_doc, supplier_order_line=sol,
                                           line_cost=cost, invoice=inv, user_modified=self.copro)
        caught = False
        try:
            pac_doc_line.save()
        except AssertionError:
            caught = True
        assert caught

    def test_stock_storage_of_orders_one_order(self):
        order = Order(user_modified=self.copro, customer=self.customer)
        order.save()
        orderlines = []
        NUMBER_ORDERED = 2
        OrderLine.add_orderlines_to_list(orderlines, number=NUMBER_ORDERED, wishable_type=self.article_type,
                                         price=Price(amount=Decimal(1.55), currency=Currency("EUR")), user=self.copro)
        Order.make_order(order, orderlines, self.copro)
        NUMBER_SUPPLIER_ORDERED = 2
        SupplierOrder.create_supplier_order(user_modified=self.copro, supplier=self.supplier,
                                            articles_ordered=[[self.article_type, NUMBER_SUPPLIER_ORDERED, self.cost]])
        pac_doc = PackingDocument(supplier=self.supplier, supplier_identifier="Foo", user_modified=self.copro)
        pac_doc.save()
        sols = SupplierOrderLine.objects.all()
        inv = Invoice(user_modified=self.copro, supplier=self.supplier)
        inv.save()
        cost = Cost(amount=Decimal(2.78), use_system_currency=True)
        # Two lines, but one order
        NUMBER_BATCHED = 2
        pac_doc_line_1 = PackingDocumentLine(article_type=self.article_type,
                                           packing_document=pac_doc, supplier_order_line=sols[0],
                                           line_cost_after_invoice=cost, invoice=inv, user_modified=self.copro)
        pac_doc_line_2 = PackingDocumentLine(article_type=self.article_type,
                                             packing_document=pac_doc, supplier_order_line=sols[1],
                                             line_cost_after_invoice=cost, invoice=inv, user_modified=self.copro)
        pac_doc_line_1.save()
        pac_doc_line_2.save()
        stock = Stock.objects.all()
        assert len(stock) == 1
        st_line = stock[0]
        assert st_line.count == NUMBER_BATCHED
        assert st_line.labeltype == OrderLabel._labeltype
        assert st_line.labelkey == 1 # Order identifier/pk

    def test_stock_storage_of_orders_more_orders(self):
        order_1 = Order(user_modified=self.copro, customer=self.customer)
        order_2 = Order(user_modified=self.copro, customer=self.customer)
        orderlines = []
        NUMBER_ORDERED_1 = 1
        NUMBER_ORDERED_2 = 1
        NUMBER_ORDERED = NUMBER_ORDERED_1 + NUMBER_ORDERED_2
        OrderLine.add_orderlines_to_list(orderlines, number=NUMBER_ORDERED_1, wishable_type=self.article_type,
                                         price=Price(amount=Decimal(1.55), currency=Currency("EUR")), user=self.copro)
        Order.make_order(order_1, orderlines, self.copro)
        orderlines = []
        OrderLine.add_orderlines_to_list(orderlines, number=NUMBER_ORDERED_2, wishable_type=self.article_type,
                                         price=Price(amount=Decimal(1.55), currency=Currency("EUR")), user=self.copro)
        Order.make_order(order_2, orderlines, self.copro)
        NUMBER_SUPPLIER_ORDERED = NUMBER_ORDERED
        SupplierOrder.create_supplier_order(user_modified=self.copro, supplier=self.supplier,
                                            articles_ordered=[[self.article_type, NUMBER_SUPPLIER_ORDERED, self.cost]])
        pac_doc = PackingDocument(supplier=self.supplier, supplier_identifier="Foo", user_modified=self.copro)
        pac_doc.save()
        sols = SupplierOrderLine.objects.all()
        inv = Invoice(user_modified=self.copro, supplier=self.supplier)
        inv.save()
        cost = Cost(amount=Decimal(2.78), use_system_currency=True)
        # Two lines, but one order
        NUMBER_BATCHED = len(sols)
        assert NUMBER_BATCHED == 2
        pac_doc_line_1 = PackingDocumentLine(article_type=self.article_type,
                                             packing_document=pac_doc, supplier_order_line=sols[0],
                                             line_cost_after_invoice=cost, invoice=inv, user_modified=self.copro)
        pac_doc_line_2 = PackingDocumentLine(article_type=self.article_type,
                                             packing_document=pac_doc, supplier_order_line=sols[1],
                                             line_cost_after_invoice=cost, invoice=inv, user_modified=self.copro)
        pac_doc_line_1.save()
        pac_doc_line_2.save()
        stock = Stock.objects.all()
        assert len(stock) == 2
        for st in stock:
            assert st.count == 1
            assert st.labeltype == OrderLabel._labeltype

        assert stock[0].labelkey == 1  # Order identifier/pk
        assert stock[1].labelkey == 2  # Order identifier/pk

    def test_stock_storage_of_orders_more_prices(self):
        order_1 = Order(user_modified=self.copro, customer=self.customer)
        orderlines = []
        NUMBER_ORDERED_1 = 2
        NUMBER_ORDERED = NUMBER_ORDERED_1
        OrderLine.add_orderlines_to_list(orderlines, number=NUMBER_ORDERED_1, wishable_type=self.article_type,
                                         price=Price(amount=Decimal(1.55), currency=Currency("EUR")), user=self.copro)
        Order.make_order(order_1, orderlines, self.copro)
        NUMBER_SUPPLIER_ORDERED = NUMBER_ORDERED
        SupplierOrder.create_supplier_order(user_modified=self.copro, supplier=self.supplier,
                                            articles_ordered=[[self.article_type, NUMBER_SUPPLIER_ORDERED, self.cost]])
        pac_doc = PackingDocument(supplier=self.supplier, supplier_identifier="Foo", user_modified=self.copro)
        pac_doc.save()
        sols = SupplierOrderLine.objects.all()
        inv = Invoice(user_modified=self.copro, supplier=self.supplier)
        inv.save()
        cost_1 = Cost(amount=Decimal(2.78), use_system_currency=True)
        cost_2 = Cost(amount=Decimal(2.79), use_system_currency=True)
        # One order and supplier order
        pac_doc_line_1 = PackingDocumentLine(article_type=self.article_type,
                                             packing_document=pac_doc, supplier_order_line=sols[0],
                                             line_cost_after_invoice=cost_1, invoice=inv, user_modified=self.copro)
        pac_doc_line_2 = PackingDocumentLine(article_type=self.article_type,
                                             packing_document=pac_doc, supplier_order_line=sols[1],
                                             line_cost_after_invoice=cost_2, invoice=inv, user_modified=self.copro)
        pac_doc_line_1.save()
        pac_doc_line_2.save()
        stock = Stock.objects.all()
        assert len(stock) == 1
        for st in stock:
            assert st.count == 2
            assert st.labeltype == OrderLabel._labeltype
            assert st.labelkey == 1 # Order pk

    def test_packingdocumentline_storage_without_stock_mod(self):
        order = Order(user_modified=self.copro, customer=self.customer)
        order.save()
        orderlines = []
        OrderLine.add_orderlines_to_list(orderlines, number=1, wishable_type=self.article_type,
                                         price=Price(amount=Decimal(1.55), currency=Currency("EUR")), user=self.copro)
        Order.make_order(order, orderlines, self.copro)
        SupplierOrder.create_supplier_order(user_modified=self.copro, supplier=self.supplier,
                                            articles_ordered=[[self.article_type, 1, self.cost]])
        pac_doc = PackingDocument(supplier=self.supplier, supplier_identifier="Foo", user_modified=self.copro)
        pac_doc.save()
        sol = SupplierOrderLine.objects.get()
        pac_doc_line = PackingDocumentLine(article_type=self.article_type,
                                           packing_document=pac_doc, supplier_order_line=sol, user_modified=self.copro)
        pac_doc_line.save(mod_stock=False)
        st = Stock.objects.all()
        assert len(st) == 0


class DistributionTests(TestCase):

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

        self.cost = Cost(currency=Currency('EUR'), amount=Decimal(1.23))
        self.cost2 = Cost(currency=Currency('EUR'), amount=Decimal(1.24))

    def test_distribution_simple_no_invoice(self):
        order_1 = Order(user_modified=self.copro, customer=self.customer)
        order_2 = Order(user_modified=self.copro, customer=self.customer)
        orderlines = []
        NUMBER_ORDERED_1 = 1
        NUMBER_ORDERED_2 = 1
        NUMBER_ORDERED = NUMBER_ORDERED_1 + NUMBER_ORDERED_2
        OrderLine.add_orderlines_to_list(orderlines, number=NUMBER_ORDERED_1, wishable_type=self.article_type,
                                         price=Price(amount=Decimal(1.55), currency=Currency("EUR")), user=self.copro)
        Order.make_order(order_1, orderlines, self.copro)
        orderlines = []
        OrderLine.add_orderlines_to_list(orderlines, number=NUMBER_ORDERED_2, wishable_type=self.article_type,
                                         price=Price(amount=Decimal(1.55), currency=Currency("EUR")), user=self.copro)
        Order.make_order(order_2, orderlines, self.copro)
        NUMBER_SUPPLIER_ORDERED = NUMBER_ORDERED
        SupplierOrder.create_supplier_order(user_modified=self.copro, supplier=self.supplier,
                                            articles_ordered=[[self.article_type, NUMBER_SUPPLIER_ORDERED, self.cost]])
        sols = SupplierOrderLine.objects.all()
        pac_doc_line_1 = PackingDocumentLine(article_type=self.article_type,
                                             supplier_order_line=sols[0]
                                             )
        pac_doc_line_2 = PackingDocumentLine(article_type=self.article_type,
                                             supplier_order_line=sols[1]
                                             )
        distribution = []
        distribution.append(pac_doc_line_1)
        distribution.append(pac_doc_line_2)
        DistributionStrategy.distribute(supplier=self.supplier, user=self.copro,
                                        distribution=distribution, document_identifier="A", indirect=True)
        pdls = PackingDocumentLine.objects.all()
        assert len(pdls) == 2
        assert pdls[0].packing_document == pdls[1].packing_document
        assert not (pdls[0].supplier_order_line == pdls[1].supplier_order_line)
        for pdl in pdls:
            assert pdl.line_cost == self.cost
            assert pdl.line_cost_after_invoice is None

    def test_distribution_illegal_final_cost_no_invoice(self):
        order_1 = Order(user_modified=self.copro, customer=self.customer)
        order_2 = Order(user_modified=self.copro, customer=self.customer)
        orderlines = []
        NUMBER_ORDERED_1 = 1
        NUMBER_ORDERED_2 = 1
        NUMBER_ORDERED = NUMBER_ORDERED_1 + NUMBER_ORDERED_2
        OrderLine.add_orderlines_to_list(orderlines, number=NUMBER_ORDERED_1, wishable_type=self.article_type,
                                         price=Price(amount=Decimal(1.55), currency=Currency("EUR")), user=self.copro)
        Order.make_order(order_1, orderlines, self.copro)
        orderlines = []
        OrderLine.add_orderlines_to_list(orderlines, number=NUMBER_ORDERED_2, wishable_type=self.article_type,
                                         price=Price(amount=Decimal(1.55), currency=Currency("EUR")), user=self.copro)
        Order.make_order(order_2, orderlines, self.copro)
        NUMBER_SUPPLIER_ORDERED = NUMBER_ORDERED
        SupplierOrder.create_supplier_order(user_modified=self.copro, supplier=self.supplier,
                                            articles_ordered=[[self.article_type, NUMBER_SUPPLIER_ORDERED, self.cost]])
        sols = SupplierOrderLine.objects.all()
        pac_doc_line_1 = PackingDocumentLine(article_type=self.article_type,
                                             supplier_order_line=sols[0],
                                             line_cost_after_invoice=self.cost
                                             )
        distribution = []
        distribution.append(pac_doc_line_1)
        caught = False
        try:
            DistributionStrategy.distribute(supplier=self.supplier, user=self.copro,
                                        distribution=distribution, document_identifier="A", indirect=True)
        except AssertionError:
            caught = True

        assert caught

    def test_distribution_illegal_invoice_identifier(self):
        order_1 = Order(user_modified=self.copro, customer=self.customer)
        order_2 = Order(user_modified=self.copro, customer=self.customer)
        orderlines = []
        NUMBER_ORDERED_1 = 1
        NUMBER_ORDERED_2 = 1
        NUMBER_ORDERED = NUMBER_ORDERED_1 + NUMBER_ORDERED_2
        OrderLine.add_orderlines_to_list(orderlines, number=NUMBER_ORDERED_1, wishable_type=self.article_type,
                                         price=Price(amount=Decimal(1.55), currency=Currency("EUR")), user=self.copro)
        Order.make_order(order_1, orderlines, self.copro)
        orderlines = []
        OrderLine.add_orderlines_to_list(orderlines, number=NUMBER_ORDERED_2, wishable_type=self.article_type,
                                         price=Price(amount=Decimal(1.55), currency=Currency("EUR")), user=self.copro)
        Order.make_order(order_2, orderlines, self.copro)
        NUMBER_SUPPLIER_ORDERED = NUMBER_ORDERED
        SupplierOrder.create_supplier_order(user_modified=self.copro, supplier=self.supplier,
                                            articles_ordered=[[self.article_type, NUMBER_SUPPLIER_ORDERED, self.cost]])
        sols = SupplierOrderLine.objects.all()
        pac_doc_line_1 = PackingDocumentLine(article_type=self.article_type,
                                             supplier_order_line=sols[0]
                                             )
        distribution = []
        distribution.append(pac_doc_line_1)
        caught = False
        try:
            DistributionStrategy.distribute(supplier=self.supplier, user=self.copro,
                                        distribution=distribution, document_identifier="A", invoice_identifier="B"
                                            ,indirect=True)
        except AssertionError:
            caught = True

        assert caught

    def test_distribution_simple_with_invoice(self):
        order_1 = Order(user_modified=self.copro, customer=self.customer)
        order_2 = Order(user_modified=self.copro, customer=self.customer)
        orderlines = []
        NUMBER_ORDERED_1 = 1
        NUMBER_ORDERED_2 = 1
        NUMBER_ORDERED = NUMBER_ORDERED_1 + NUMBER_ORDERED_2
        OrderLine.add_orderlines_to_list(orderlines, number=NUMBER_ORDERED_1, wishable_type=self.article_type,
                                         price=Price(amount=Decimal(1.55), currency=Currency("EUR")), user=self.copro)
        Order.make_order(order_1, orderlines, self.copro)
        orderlines = []
        OrderLine.add_orderlines_to_list(orderlines, number=NUMBER_ORDERED_2, wishable_type=self.article_type,
                                         price=Price(amount=Decimal(1.55), currency=Currency("EUR")), user=self.copro)
        Order.make_order(order_2, orderlines, self.copro)
        NUMBER_SUPPLIER_ORDERED = NUMBER_ORDERED
        SupplierOrder.create_supplier_order(user_modified=self.copro, supplier=self.supplier,
                                            articles_ordered=[[self.article_type, NUMBER_SUPPLIER_ORDERED, self.cost]])
        sols = SupplierOrderLine.objects.all()
        pac_doc_line_1 = PackingDocumentLine(article_type=self.article_type,
                                             supplier_order_line=sols[0], line_cost_after_invoice=self.cost2
                                             )
        pac_doc_line_2 = PackingDocumentLine(article_type=self.article_type,
                                             supplier_order_line=sols[1]
                                             )
        distribution = []
        distribution.append(pac_doc_line_1)
        distribution.append(pac_doc_line_2)
        DistributionStrategy.distribute(supplier=self.supplier, user=self.copro,
                                        distribution=distribution, document_identifier="A",
                                        invoice_identifier="B", indirect=True)
        pdls = PackingDocumentLine.objects.all()
        assert len(pdls) == 2
        assert pdls[0].packing_document == pdls[1].packing_document
        assert not (pdls[0].supplier_order_line == pdls[1].supplier_order_line)
        for pdl in pdls:
            assert pdl.line_cost == self.cost
        assert pdls[0].line_cost_after_invoice == self.cost2
        assert pdls[0].invoice is not None

    def test_first_supplier_order_strategy_no_cost(self):
        order_1 = Order(user_modified=self.copro, customer=self.customer)
        orderlines = []
        NUMBER_ORDERED_1 = 10
        OrderLine.add_orderlines_to_list(orderlines, number=NUMBER_ORDERED_1, wishable_type=self.article_type,
                                         price=Price(amount=Decimal(1.55), currency=Currency("EUR")), user=self.copro)
        Order.make_order(order_1, orderlines, self.copro)
        SupplierOrder.create_supplier_order(user_modified=self.copro, supplier=self.supplier,
                                            articles_ordered=[[self.article_type, NUMBER_ORDERED_1, self.cost]])

        supply = [[self.article_type, 10]]
        dist = FirstSupplierOrderStrategy.get_distribution(supply, supplier=self.supplier)
        for pac_doc_line in dist:
            assert pac_doc_line.line_cost == self.cost
            assert pac_doc_line.invoice is None
            assert pac_doc_line.line_cost_after_invoice is None
            assert pac_doc_line.article_type == self.article_type

    def test_first_supplier_order_strategy_no_cost_lesser_amount(self):
        order_1 = Order(user_modified=self.copro, customer=self.customer)
        orderlines = []
        NUMBER_ORDERED_1 = 10
        OrderLine.add_orderlines_to_list(orderlines, number=NUMBER_ORDERED_1, wishable_type=self.article_type,
                                         price=Price(amount=Decimal(1.55), currency=Currency("EUR")), user=self.copro)
        Order.make_order(order_1, orderlines, self.copro)
        SupplierOrder.create_supplier_order(user_modified=self.copro, supplier=self.supplier,
                                            articles_ordered=[[self.article_type, NUMBER_ORDERED_1, self.cost]])

        supply = [[self.article_type, 8]]
        dist = FirstSupplierOrderStrategy.get_distribution(supply, supplier=self.supplier)
        for i in range(0, len(dist)):
            assert dist[i].supplier_order_line.pk == i+1
            assert dist[i].line_cost == self.cost
            assert dist[i].invoice is None
            assert dist[i].line_cost_after_invoice is None
            assert dist[i].article_type == self.article_type

    def test_first_supplier_order_strategy_no_cost_with_wishes(self):
        STOCK_WISH = 5
        StockWish.create_stock_wish(user_modified=self.copro, articles_ordered=[[self.article_type, STOCK_WISH]])
        order_1 = Order(user_modified=self.copro, customer=self.customer)
        SupplierOrder.create_supplier_order(user_modified=self.copro, supplier=self.supplier,
                                            articles_ordered=[[self.article_type, STOCK_WISH, self.cost]])
        orderlines = []
        NUMBER_ORDERED_1 = 10
        OrderLine.add_orderlines_to_list(orderlines, number=NUMBER_ORDERED_1, wishable_type=self.article_type,
                                         price=Price(amount=Decimal(1.55), currency=Currency("EUR")), user=self.copro)
        Order.make_order(order_1, orderlines, self.copro)
        SupplierOrder.create_supplier_order(user_modified=self.copro, supplier=self.supplier,
                                            articles_ordered=[[self.article_type, NUMBER_ORDERED_1, self.cost]])

        supply = [[self.article_type, 8]]
        dist = FirstSupplierOrderStrategy.get_distribution(supply, supplier=self.supplier)
        for i in range(0, STOCK_WISH):
            assert dist[i].supplier_order_line.pk == i+1
            assert dist[i].line_cost == self.cost
            assert dist[i].invoice is None
            assert dist[i].line_cost_after_invoice is None
            assert dist[i].article_type == self.article_type
            assert dist[i].supplier_order_line.order_line is None
        for i in range(STOCK_WISH+1, len(dist)):
            assert dist[i].supplier_order_line.pk == i + 1
            assert dist[i].line_cost == self.cost
            assert dist[i].invoice is None
            assert dist[i].line_cost_after_invoice is None
            assert dist[i].article_type == self.article_type
            assert dist[i].supplier_order_line.order_line is not None

    def test_first_supplier_order_strategy_with_cost(self):
        order_1 = Order(user_modified=self.copro, customer=self.customer)
        orderlines = []
        NUMBER_ORDERED_1 = 10
        OrderLine.add_orderlines_to_list(orderlines, number=NUMBER_ORDERED_1, wishable_type=self.article_type,
                                         price=Price(amount=Decimal(1.55), currency=Currency("EUR")), user=self.copro)
        Order.make_order(order_1, orderlines, self.copro)
        SupplierOrder.create_supplier_order(user_modified=self.copro, supplier=self.supplier,
                                            articles_ordered=[[self.article_type, NUMBER_ORDERED_1, self.cost]])
        NON_COST = 8
        WITH_COST = 2
        supply = [[self.article_type, NON_COST], [self.article_type, WITH_COST, self.cost2]]
        dist = FirstSupplierOrderStrategy.get_distribution(supply, supplier=self.supplier)
        cost_counted = 0
        for dis in dist:
            if dis.line_cost_after_invoice == self.cost2:
                cost_counted += 1
        assert cost_counted == WITH_COST

    def test_second_strategy_orders_only_no_cost(self):
        order_1 = Order(user_modified=self.copro, customer=self.customer)
        orderlines = []
        NUMBER_ORDERED_1 = 10
        OrderLine.add_orderlines_to_list(orderlines, number=NUMBER_ORDERED_1, wishable_type=self.article_type,
                                         price=Price(amount=Decimal(1.55), currency=Currency("EUR")), user=self.copro)
        Order.make_order(order_1, orderlines, self.copro)
        SupplierOrder.create_supplier_order(user_modified=self.copro, supplier=self.supplier,
                                            articles_ordered=[[self.article_type, NUMBER_ORDERED_1, self.cost]])
        a = FirstCustomersDateTimeThenStockDateTime.get_distribution([[self.article_type, 10]], self.supplier)
        for i in range(0,len(a)):
            assert a[i].line_cost == self.cost
            assert a[i].supplier_order_line.pk == i+1
            assert a[i].article_type == self.article_type
            assert a[i].line_cost_after_invoice is None
            assert a[i].invoice is None
            assert not hasattr(a[i], 'packing_document' ) or a[i].packing_document is None

    def test_second_strategy_orders_only_with_cost(self):
        order_1 = Order(user_modified=self.copro, customer=self.customer)
        orderlines = []
        NUMBER_ORDERED_1 = 10
        OrderLine.add_orderlines_to_list(orderlines, number=NUMBER_ORDERED_1, wishable_type=self.article_type,
                                         price=Price(amount=Decimal(1.55), currency=Currency("EUR")), user=self.copro)
        Order.make_order(order_1, orderlines, self.copro)
        SupplierOrder.create_supplier_order(user_modified=self.copro, supplier=self.supplier,
                                            articles_ordered=[[self.article_type, NUMBER_ORDERED_1, self.cost]])
        a = FirstCustomersDateTimeThenStockDateTime.get_distribution([[self.article_type, 10, self.cost2]], self.supplier)
        for i in range(0, len(a)):
            assert a[i].line_cost == self.cost
            assert a[i].supplier_order_line.pk == i+1
            assert a[i].article_type == self.article_type
            assert a[i].line_cost_after_invoice == self.cost2
            assert a[i].invoice is None
            assert not hasattr(a[i], 'packing_document' ) or a[i].packing_document is None

    def test_second_strategy_mixed_no_cost(self):
        STOCK_WISH = 5
        StockWish.create_stock_wish(self.copro, [[self.article_type, STOCK_WISH]])
        order_1 = Order(user_modified=self.copro, customer=self.customer)
        orderlines = []
        NUMBER_ORDERED_1 = 5
        TOTAL_ORDERED = 10
        OrderLine.add_orderlines_to_list(orderlines, number=NUMBER_ORDERED_1, wishable_type=self.article_type,
                                         price=Price(amount=Decimal(1.55), currency=Currency("EUR")), user=self.copro)
        Order.make_order(order_1, orderlines, self.copro)
        SupplierOrder.create_supplier_order(user_modified=self.copro, supplier=self.supplier,
                                            articles_ordered=[[self.article_type, TOTAL_ORDERED, self.cost]])
        a = FirstCustomersDateTimeThenStockDateTime.get_distribution([[self.article_type, 10, self.cost2]], self.supplier)
        for i in range(0, len(a)):
            if i< STOCK_WISH:
                assert a[i].supplier_order_line.order_line is not None
            else:
                assert a[i].supplier_order_line.order_line is None
            assert a[i].line_cost == self.cost
            assert a[i].supplier_order_line.pk == i+1
            assert a[i].article_type == self.article_type
            assert a[i].line_cost_after_invoice == self.cost2
            assert a[i].invoice is None
            assert not hasattr(a[i], 'packing_document' ) or a[i].packing_document is None





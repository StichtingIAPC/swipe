from decimal import Decimal

from django.test import TestCase
from tools.testing import TestData
from swipe.settings import USED_CURRENCY

from article.models import ArticleType
from assortment.models import AssortmentArticleBranch
from crm.models import Person, User
from logistics.models import SupplierOrder, StockWish
from money.models import VAT, AccountingGroup, Price, Currency, Cost, Money, VATPeriod
from order.models import OrderLine, Order
from stock.models import Stock, StockChange
from supplication import models
from supplication.models import PackingDocument, PackingDocumentLine, SupplierOrderLine, Invoice, OrderLabel, \
    DistributionStrategy, FirstSupplierOrderStrategy, \
    FirstCustomersDateTimeThenStockDateTime, SerialNumber, IncorrectDataError
from supplier.models import Supplier, ArticleTypeSupplier


# Create your tests here.
class SimpleClassTests(TestCase, TestData):

    def setUp(self):
        self.setup_base_data()
        self.vat_group = self.vat_group_high
        self.price = Price(amount=Decimal("1.00"), use_system_currency=True)
        self.currency = Currency(iso="USD")

        self.acc_group = self.accounting_group_components

        self.branch = self.branch_1

        self.article_type = self.articletype_1
        self.at2 = self.articletype_2
        self.at3 = ArticleType(accounting_group=self.acc_group, name="Foo3", branch=self.branch)
        self.at3.save()

        cost = Cost(amount=Decimal(1), use_system_currency=True)

        self.supplier = self.supplier_1

        ats = self.articletypesupplier_article_1
        ats2 = self.articletypesupplier_article_2

        self.customer = self.customer_person_1

        self.copro = self.user_1

        self.cost = Cost(currency=Currency(USED_CURRENCY), amount=Decimal(1.23))

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
        self.assertEquals(pd.line_cost, pd.supplier_order_line.line_cost)

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
        self.assertEquals(pac_doc_line.invoice, inv)
        self.assertEquals(pac_doc_line.line_cost, self.cost)
        self.assertEquals(pac_doc_line.line_cost_after_invoice, cost)

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
        with self.assertRaises(models.IncorrectDataError):
            pac_doc_line.save()

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
        with self.assertRaises(models.InvalidDataError):
            pac_doc_line.save()

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
        self.assertEquals(len(stock), 1)
        st_line = stock[0]
        self.assertEquals(st_line.count, NUMBER_BATCHED)
        self.assertEquals(st_line.labeltype, OrderLabel.labeltype)
        self.assertEquals(st_line.labelkey, 1)  # Order identifier/pk

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
        self.assertEquals(NUMBER_BATCHED, 2)
        pac_doc_line_1 = PackingDocumentLine(article_type=self.article_type,
                                             packing_document=pac_doc, supplier_order_line=sols[0],
                                             line_cost_after_invoice=cost, invoice=inv, user_modified=self.copro)
        pac_doc_line_2 = PackingDocumentLine(article_type=self.article_type,
                                             packing_document=pac_doc, supplier_order_line=sols[1],
                                             line_cost_after_invoice=cost, invoice=inv, user_modified=self.copro)
        pac_doc_line_1.save()
        pac_doc_line_2.save()
        stock = Stock.objects.all()
        self.assertEquals(len(stock), 2)
        for st in stock:
            self.assertEquals(st.count, 1)
            self.assertEquals(st.labeltype, OrderLabel.labeltype)

        self.assertEquals(stock[0].labelkey, 1)  # Order identifier/pk
        self.assertEquals(stock[1].labelkey, 2)  # Order identifier/pk

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
        self.assertEquals(len(stock), 1)
        for st in stock:
            self.assertEquals(st.count, 2)
            self.assertEquals(st.labeltype, OrderLabel.labeltype)
            self.assertEquals(st.labelkey, 1)  # Order pk

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
        self.assertEquals(len(st), 0)


# noinspection PyPackageRequirements,PyPackageRequirements
class DistributionTests(TestCase, TestData):

    def setUp(self):
        self.setup_base_data()
        self.vat_group = self.vat_group_high
        self.price = Price(amount=Decimal("1.00"), use_system_currency=True)
        self.currency = Currency(iso="USD")

        self.acc_group = self.accounting_group_components

        self.branch = self.branch_1

        self.article_type = self.articletype_1
        self.at2 = self.articletype_2
        self.at3 = ArticleType(accounting_group=self.acc_group, name="Foo3", branch=self.branch)
        self.at3.save()

        cost = Cost(amount=Decimal(1), use_system_currency=True)

        self.supplier = self.supplier_1
        ats = self.articletypesupplier_article_1
        ats2 = self.articletypesupplier_article_2
        self.money = Money(amount=Decimal(3.32), currency=self.currency)

        self.customer = self.customer_person_1

        self.copro = self.user_1

        self.cost = Cost(currency=Currency(USED_CURRENCY), amount=Decimal(1.23))
        self.cost2 = Cost(currency=Currency(USED_CURRENCY), amount=Decimal(1.24))

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
                                             supplier_order_line=sols[0])
        pac_doc_line_2 = PackingDocumentLine(article_type=self.article_type,
                                             supplier_order_line=sols[1])
        distribution = [pac_doc_line_1, pac_doc_line_2]
        DistributionStrategy.distribute(supplier=self.supplier, user=self.copro,
                                        distribution=distribution, document_identifier="A", indirect=True)
        pdls = PackingDocumentLine.objects.all()
        self.assertEquals(len(pdls), 2)
        self.assertEquals(pdls[0].packing_document, pdls[1].packing_document)
        self.assertNotEqual(pdls[0].supplier_order_line, pdls[1].supplier_order_line)
        for pdl in pdls:
            self.assertEquals(pdl.line_cost, self.cost)
            self.assertIsNone(pdl.line_cost_after_invoice)

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
                                             line_cost_after_invoice=self.cost)
        distribution = [pac_doc_line_1]
        with self.assertRaises(models.InvalidDataError):
            DistributionStrategy.distribute(supplier=self.supplier, user=self.copro,
                                            distribution=distribution, document_identifier="A", indirect=True)

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
                                             supplier_order_line=sols[0])
        distribution = [pac_doc_line_1]
        with self.assertRaises(models.IncorrectDataError):
            DistributionStrategy.distribute(supplier=self.supplier, user=self.copro,
                                            distribution=distribution, document_identifier="A", invoice_identifier="B",
                                            indirect=True)

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
                                             supplier_order_line=sols[0], line_cost_after_invoice=self.cost2)
        pac_doc_line_2 = PackingDocumentLine(article_type=self.article_type,
                                             supplier_order_line=sols[1])
        distribution = [pac_doc_line_1, pac_doc_line_2]
        DistributionStrategy.distribute(supplier=self.supplier, user=self.copro,
                                        distribution=distribution, document_identifier="A",
                                        invoice_identifier="B", indirect=True)
        pdls = PackingDocumentLine.objects.all()
        self.assertEquals(len(pdls), 2)
        self.assertEquals(pdls[0].packing_document, pdls[1].packing_document)
        self.assertNotEqual(pdls[0].supplier_order_line, pdls[1].supplier_order_line)
        for pdl in pdls:
            self.assertEquals(pdl.line_cost, self.cost)
        self.assertEquals(pdls[0].line_cost_after_invoice, self.cost2)
        self.assertIsNotNone(pdls[0].invoice)

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
            self.assertEquals(pac_doc_line.line_cost, self.cost)
            self.assertIsNone(pac_doc_line.invoice)
            self.assertIsNone(pac_doc_line.line_cost_after_invoice)
            self.assertEquals(pac_doc_line.article_type, self.article_type)

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
            self.assertEquals(dist[i].supplier_order_line.pk, i+1)
            self.assertEquals(dist[i].line_cost, self.cost)
            self.assertIsNone(dist[i].invoice)
            self.assertIsNone(dist[i].line_cost_after_invoice)
            self.assertEquals(dist[i].article_type, self.article_type)

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
            self.assertEquals(dist[i].supplier_order_line.pk, i+1)
            self.assertEquals(dist[i].line_cost, self.cost)
            self.assertIsNone(dist[i].invoice)
            self.assertIsNone(dist[i].line_cost_after_invoice)
            self.assertEquals(dist[i].article_type, self.article_type)
            self.assertIsNone(dist[i].supplier_order_line.order_line)
        for i in range(STOCK_WISH+1, len(dist)):
            self.assertEquals(dist[i].supplier_order_line.pk, i + 1)
            self.assertEquals(dist[i].line_cost, self.cost)
            self.assertIsNone(dist[i].invoice)
            self.assertIsNone(dist[i].line_cost_after_invoice)
            self.assertEquals(dist[i].article_type, self.article_type)
            self.assertIsNotNone(dist[i].supplier_order_line.order_line)

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

        self.assertEquals(cost_counted, WITH_COST)

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
            self.assertEquals(a[i].line_cost, self.cost)
            self.assertEquals(a[i].supplier_order_line.pk, i+1)
            self.assertEquals(a[i].article_type, self.article_type)
            self.assertIsNone(a[i].line_cost_after_invoice)
            self.assertIsNone(a[i].invoice)
            self.assertTrue(not hasattr(a[i], 'packing_document' ) or a[i].packing_document)

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
            self.assertEquals(a[i].line_cost, self.cost)
            self.assertEquals(a[i].supplier_order_line.pk, i+1)
            self.assertEquals(a[i].article_type, self.article_type)
            self.assertEquals(a[i].line_cost_after_invoice, self.cost2)
            self.assertIsNone(a[i].invoice)
            self.assertTrue(not hasattr(a[i], 'packing_document') or a[i].packing_document)

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
                self.assertIsNotNone(a[i].supplier_order_line.order_line)
            else:
                self.assertIsNone(a[i].supplier_order_line.order_line)
                self.assertEquals(a[i].line_cost, self.cost)

            self.assertEquals(a[i].supplier_order_line.pk, i+1)
            self.assertEquals(a[i].article_type, self.article_type)
            self.assertEquals(a[i].line_cost_after_invoice, self.cost2)
            self.assertIsNone(a[i].invoice)
            self.assertTrue(not hasattr(a[i], 'packing_document') or a[i].packing_document)

    def test_stock_change_set_generation_mixed(self):
        STOCK_WISH = 5
        StockWish.create_stock_wish(self.copro, [[self.article_type, STOCK_WISH]])
        NUMBER_ORDERED_1 = 5
        NUMBER_ORDERED_ARTICLE_2 = 5
        TOTAL_ORDERED = 10
        Order.create_order_from_wishables_combinations(self.copro, self.customer ,
                                                       [[self.article_type, NUMBER_ORDERED_1, self.price],
                                                        [self.at2, NUMBER_ORDERED_ARTICLE_2, self.price]])
        SupplierOrder.create_supplier_order(user_modified=self.copro, supplier=self.supplier,
                                            articles_ordered=[[self.article_type, TOTAL_ORDERED, self.cost],
                                                              [self.at2, NUMBER_ORDERED_ARTICLE_2, self.cost]])
        a = FirstCustomersDateTimeThenStockDateTime.get_distribution([[self.article_type, 10, self.cost2],
                                                                      [self.at2, 5, self.cost2]],
                                                                     self.supplier)
        b = DistributionStrategy.build_changeset(a)
        self.assertEquals(len(b), 3)
        for elem in b:
            if elem.get('label') is None:
                self.assertEquals(elem['article'], self.article_type)  # Stockwish are of article_type
            self.assertEquals(elem['count'], 5)  # Checks if all counts are correct
            self.assertEquals(elem['is_in'], True)  # All is in
            self.assertEquals(elem['book_value'], self.cost)  # Checks if PackingDocLines retrieve cost from SupOrdLines

    def test_stock_change_set_generation_wishes_only(self):
        STOCK_WISH_1 = 5
        STOCK_WISH_2 = 6
        StockWish.create_stock_wish(self.copro, [[self.article_type, STOCK_WISH_1], [self.at2, STOCK_WISH_2]])
        SupplierOrder.create_supplier_order(user_modified=self.copro, supplier=self.supplier,
                                            articles_ordered=[[self.article_type, STOCK_WISH_1, self.cost],
                                                              [self.at2, STOCK_WISH_2, self.cost]])
        a = FirstCustomersDateTimeThenStockDateTime.get_distribution([[self.article_type, STOCK_WISH_1, self.cost],
                                                                      [self.at2, STOCK_WISH_2, self.cost]],
                                                                     supplier=self.supplier)
        b = DistributionStrategy.build_changeset(a)
        for elem in b:
            self.assertIsNone(elem.get('label'))
            self.assertEquals(elem['book_value'], self.cost)
            self.assertEquals(elem['is_in'], True)
            if elem['article'] == self.article_type:
                self.assertEquals(elem['count'], STOCK_WISH_1)
            else:
                self.assertEquals(elem['count'], STOCK_WISH_2)

    def test_stock_change_set_generation_orders_only(self):
        NUMBER_ORDERED_1 = 5
        NUMBER_ORDERED_ARTICLE_2 = 5
        Order.create_order_from_wishables_combinations(self.copro, self.customer ,
                                                       [[self.article_type, NUMBER_ORDERED_1, self.price],
                                                        [self.at2, NUMBER_ORDERED_ARTICLE_2, self.price]])
        Order.create_order_from_wishables_combinations(self.copro, self.customer,
                                                       [[self.article_type, NUMBER_ORDERED_1, self.price],
                                                        [self.at2, NUMBER_ORDERED_ARTICLE_2, self.price]])
        SupplierOrder.create_supplier_order(user_modified=self.copro, supplier=self.supplier,
                                            articles_ordered=[[self.article_type, NUMBER_ORDERED_1*2, self.cost],
                                                              [self.at2, NUMBER_ORDERED_ARTICLE_2*2, self.cost]])
        a = FirstCustomersDateTimeThenStockDateTime.get_distribution([[self.article_type, NUMBER_ORDERED_1*2],
                                                                      [self.at2, NUMBER_ORDERED_ARTICLE_2*2]],
                                                                     self.supplier)
        b = DistributionStrategy.build_changeset(a)
        self.assertEquals(len(b), 4)
        for elem in b:
            self.assertIsNotNone(elem.get('label'))
            self.assertTrue(elem['article'] == self.article_type or elem['article'] == self.at2)
            self.assertEquals(elem['count'], 5)  # Checks if all counts are correct
            self.assertEquals(elem['is_in'], True)  # All is in
            self.assertEquals(elem['book_value'], self.cost)  # Checks if PackingDocLines retrieve cost from SupOrdLines

    def test_distribute_no_invoice(self):
        STOCK_WISH = 5
        StockWish.create_stock_wish(self.copro, [[self.article_type, STOCK_WISH]])
        NUMBER_ORDERED_1 = 5
        NUMBER_ORDERED_ARTICLE_2 = 5
        TOTAL_ORDERED = 10
        Order.create_order_from_wishables_combinations(self.copro, self.customer ,
                                                       [[self.article_type, NUMBER_ORDERED_1, self.price],
                                                        [self.at2, NUMBER_ORDERED_ARTICLE_2, self.price]])
        SupplierOrder.create_supplier_order(user_modified=self.copro, supplier=self.supplier,
                                            articles_ordered=[[self.article_type, TOTAL_ORDERED, self.cost],
                                                              [self.at2, NUMBER_ORDERED_ARTICLE_2, self.cost]])
        a = FirstCustomersDateTimeThenStockDateTime.get_distribution([[self.article_type, 10], [self.at2, 5]],
                                                                     self.supplier)
        DistributionStrategy.distribute(distribution=a, user=self.copro, supplier=self.supplier, indirect=True,
                                        document_identifier="Dloa")
        pdls = PackingDocumentLine.objects.all()
        PackingDocument.objects.get()
        stock = Stock.objects.all()
        counted_stock_lines_in_order = 0
        for line in stock:
            self.assertEquals(line.count, 5)
            if line.label is not None:
                counted_stock_lines_in_order += 1
        self.assertEquals(counted_stock_lines_in_order, 2)
        self.assertEquals(len(stock), 3)

        self.assertEquals(len(pdls), 15)
        inv = Invoice.objects.all()
        self.assertEquals(len(inv), 0)
        stc = StockChange.objects.all()
        self.assertEquals(len(stc), 15)

    def test_distribute_with_invoice(self):
        STOCK_WISH = 5
        StockWish.create_stock_wish(self.copro, [[self.article_type, STOCK_WISH]])
        NUMBER_ORDERED_1 = 5
        NUMBER_ORDERED_ARTICLE_2 = 5
        TOTAL_ORDERED = 10
        Order.create_order_from_wishables_combinations(self.copro, self.customer ,
                                                       [[self.article_type, NUMBER_ORDERED_1, self.price],
                                                        [self.at2, NUMBER_ORDERED_ARTICLE_2, self.price]])
        SupplierOrder.create_supplier_order(user_modified=self.copro, supplier=self.supplier,
                                            articles_ordered=[[self.article_type, TOTAL_ORDERED, self.cost],
                                                              [self.at2, NUMBER_ORDERED_ARTICLE_2, self.cost]])
        a = FirstCustomersDateTimeThenStockDateTime.get_distribution([[self.article_type, 10, self.cost2],
                                                                      [self.at2, 5]],
                                                                     self.supplier)
        DistributionStrategy.distribute(distribution=a, user=self.copro, supplier=self.supplier, indirect=True,
                                        document_identifier="Dloa", invoice_identifier="Bar")
        pdls = PackingDocumentLine.objects.all()
        PackingDocument.objects.get()
        stock = Stock.objects.all()
        counted_stock_lines_in_order = 0
        for line in stock:
            self.assertEquals(line.count, 5)
            if line.label is not None:
                counted_stock_lines_in_order += 1
        self.assertEquals(counted_stock_lines_in_order, 2)
        self.assertEquals(len(stock), 3)

        self.assertEquals(len(pdls), 15)
        inv = Invoice.objects.all()
        self.assertEquals(len(inv), 1)
        stc = StockChange.objects.all()
        self.assertEquals(len(stc), 15)

    def test_distribute_fail_cost_without_invoice(self):
        STOCK_WISH = 5
        StockWish.create_stock_wish(self.copro, [[self.article_type, STOCK_WISH]])
        NUMBER_ORDERED_1 = 5
        NUMBER_ORDERED_ARTICLE_2 = 5
        TOTAL_ORDERED = 10
        Order.create_order_from_wishables_combinations(self.copro, self.customer ,
                                                       [[self.article_type, NUMBER_ORDERED_1, self.price],
                                                        [self.at2, NUMBER_ORDERED_ARTICLE_2, self.price]])
        SupplierOrder.create_supplier_order(user_modified=self.copro, supplier=self.supplier,
                                            articles_ordered=[[self.article_type, TOTAL_ORDERED, self.cost],
                                                              [self.at2, NUMBER_ORDERED_ARTICLE_2, self.cost]])
        a = FirstCustomersDateTimeThenStockDateTime.get_distribution([[self.article_type, 10, self.cost2],
                                                                      [self.at2, 5]],
                                                                     self.supplier)
        with self.assertRaises(models.InvalidDataError):
            DistributionStrategy.distribute(distribution=a, user=self.copro, supplier=self.supplier, indirect=True,
                                            document_identifier="Dloa")


class PackingDocumentCreationTests(TestCase, TestData):

    def setUp(self):
        self.setup_base_data()
        self.vat_group = self.vat_group_high
        self.price = Price(amount=Decimal("1.00"), use_system_currency=True)
        self.currency = Currency(iso="USD")

        self.acc_group = self.accounting_group_components

        self.branch = self.branch_1

        self.article_type = self.articletype_1
        self.at2 = self.articletype_2
        self.at3 = ArticleType(accounting_group=self.acc_group, name="Foo3", branch=self.branch)
        self.at3.save()

        cost = Cost(amount=Decimal(1), use_system_currency=True)

        self.supplier = self.supplier_1

        ats = self.articletypesupplier_article_1
        ats2 = self.articletypesupplier_article_2
        self.money = Money(amount=Decimal(3.32), currency=self.currency)

        self.customer = self.customer_person_1

        self.copro = self.user_1

        self.cost = Cost(currency=Currency(USED_CURRENCY), amount=Decimal(1.23))
        self.cost2 = Cost(currency=Currency(USED_CURRENCY), amount=Decimal(1.24))

    def test_verify_article_demand_pass_1(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        Order.create_order_from_wishables_combinations(self.copro, self.customer,
                                                       [[self.article_type, AMOUNT_1-1, self.price]])
        Order.create_order_from_wishables_combinations(self.copro, self.customer,
                                                       [[self.article_type, 1, self.price],
                                                        [self.at2, AMOUNT_2, self.price]])
        SupplierOrder.create_supplier_order(self.copro, self.supplier,
                                            articles_ordered=[[self.article_type, AMOUNT_1-2, self.cost],
                                                              [self.at2, AMOUNT_2, self.cost]])
        result = PackingDocument.verify_article_demand(supplier=self.supplier,
                                                       article_type_cost_combinations=[[self.article_type, AMOUNT_1-2],
                                                                                       [self.at2, AMOUNT_2]],
                                                       use_invoice=False)
        self.assertEquals(len(result), 0)

    def test_verify_article_demand_fail_size(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        Order.create_order_from_wishables_combinations(self.copro, self.customer,
                                                       [[self.article_type, AMOUNT_1-1, self.price]])
        Order.create_order_from_wishables_combinations(self.copro, self.customer,
                                                       [[self.article_type, 1, self.price],
                                                        [self.at2, AMOUNT_2, self.price]])
        SupplierOrder.create_supplier_order(self.copro, self.supplier,
                                            articles_ordered=[[self.article_type, AMOUNT_1-2, self.cost],
                                                              [self.at2, AMOUNT_2, self.cost]])
        result = PackingDocument.verify_article_demand(supplier=self.supplier,
                                                       article_type_cost_combinations=[[self.article_type, AMOUNT_1-1],
                                                                                       [self.at2, AMOUNT_2]],
                                                       use_invoice=False)
        self.assertEquals(len(result), 1)
        self.assertEquals(result[0][1], 1)

    def test_verify_article_demand_fail_supplier(self):
        AMOUNT_1 = 6
        Order.create_order_from_wishables_combinations(self.copro, self.customer,
                                                       [[self.article_type, AMOUNT_1, self.price]])
        SupplierOrder.create_supplier_order(self.copro, self.supplier,
                                            articles_ordered=[[self.article_type, AMOUNT_1, self.cost]])
        supplier2 = Supplier(name="Foorab")
        supplier2.save()
        result = PackingDocument.verify_article_demand(supplier=supplier2,
                                                       article_type_cost_combinations=[[self.article_type, AMOUNT_1]],
                                                       use_invoice=False)
        self.assertEquals(len(result), 1)
        self.assertEquals(result[0][0], self.article_type)
        self.assertEquals(result[0][1], AMOUNT_1)

    def test_verify_article_demand_fail_list(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        Order.create_order_from_wishables_combinations(self.copro, self.customer,
                                                       [[self.article_type, AMOUNT_1, self.price],
                                                        [self.at2, AMOUNT_2, self.price]])
        SupplierOrder.create_supplier_order(self.copro, self.supplier,
                                            articles_ordered=[[self.article_type, AMOUNT_1, self.cost],
                                                              [self.at2, AMOUNT_2, self.cost]])
        result = PackingDocument.verify_article_demand(supplier=self.supplier,
                                                       article_type_cost_combinations=[[self.article_type, AMOUNT_1+2],
                                                                                       [self.at2, AMOUNT_2+3]],
                                                       use_invoice=False)
        self.assertEquals(len(result), 2)
        self.assertEquals(result[0][1], 2)
        self.assertEquals(result[1][1], 3)

    def test_big_creation_function_order_only_no_invoice(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        Order.create_order_from_wishables_combinations(self.copro, self.customer,
                                                       [[self.article_type, AMOUNT_1, self.price],
                                                        [self.at2, AMOUNT_2, self.price]])
        SupplierOrder.create_supplier_order(self.copro, self.supplier,
                                            articles_ordered=[[self.article_type, AMOUNT_1, self.cost],
                                                              [self.at2, AMOUNT_2, self.cost]])
        PackingDocument.create_packing_document(user=self.copro, supplier=self.supplier,
                                                article_type_cost_combinations=[[self.article_type, AMOUNT_1],
                                                                                [self.at2, AMOUNT_2]],
                                                packing_document_name="Foo")
        st = Stock.objects.all()
        art_1 = 0
        art_2 = 0
        for line in st:
            self.assertIsInstance(line.label, OrderLabel)
            self.assertEquals(line.labelkey, 1)
            if line.article == self.article_type:
                art_1 += 1
            elif line.article == self.at2:
                art_2 += 1
            else:
                self.assertTrue(False)
        self.assertEquals(art_1, 1)
        self.assertEquals(art_2, 1)
        self.assertEquals(len(st), 2)
        inv = Invoice.objects.all()
        self.assertEquals(len(inv), 0)

    def test_big_creation_function_order_only_with_invoice(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        Order.create_order_from_wishables_combinations(self.copro, self.customer,
                                                       [[self.article_type, AMOUNT_1, self.price],
                                                        [self.at2, AMOUNT_2, self.price]])
        SupplierOrder.create_supplier_order(self.copro, self.supplier,
                                            articles_ordered=[[self.article_type, AMOUNT_1, self.cost],
                                                              [self.at2, AMOUNT_2, self.cost]])
        PackingDocument.create_packing_document(user=self.copro, supplier=self.supplier,
                                                article_type_cost_combinations=[[self.article_type, AMOUNT_1,
                                                                                 self.cost2], [self.at2, AMOUNT_2]],
                                                packing_document_name="Foo", invoice_name="Bar")
        st = Stock.objects.all()
        art_1 = 0
        art_2 = 0
        for line in st:
            self.assertIsInstance(line.label, OrderLabel)
            self.assertEquals(line.labelkey, 1)
            if line.article == self.article_type:
                art_1 += 1
            elif line.article == self.at2:
                art_2 += 1
            else:
                self.assertTrue(False)
        self.assertEquals(art_1, 1)
        self.assertEquals(art_2, 1)
        self.assertEquals(len(st), 2)
        inv = Invoice.objects.all()
        self.assertEquals(len(inv), 1)

    def test_big_creation_function_order_only_fail_cost_no_invoice(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        Order.create_order_from_wishables_combinations(self.copro, self.customer,
                                                       [[self.article_type, AMOUNT_1, self.price],
                                                        [self.at2, AMOUNT_2, self.price]])
        SupplierOrder.create_supplier_order(self.copro, self.supplier,
                                            articles_ordered=[[self.article_type, AMOUNT_1, self.cost],
                                                              [self.at2, AMOUNT_2, self.cost]])
        with self.assertRaises(models.InvalidDataError):
            PackingDocument.create_packing_document(user=self.copro, supplier=self.supplier,
                                                    article_type_cost_combinations=[[self.article_type, AMOUNT_1,
                                                                                     self.cost2],[self.at2, AMOUNT_2]],
                                                    packing_document_name="Foo")

    def test_big_creation_function_stock_only_no_invoice(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        StockWish.create_stock_wish(user_modified=self.copro, articles_ordered=[[self.article_type, AMOUNT_1],
                                                                                [self.at2, AMOUNT_2]])
        SupplierOrder.create_supplier_order(self.copro, self.supplier,
                                            articles_ordered=[[self.article_type, AMOUNT_1, self.cost],
                                                              [self.at2, AMOUNT_2, self.cost]])
        PackingDocument.create_packing_document(user=self.copro, supplier=self.supplier,
                                                article_type_cost_combinations=[[self.article_type, AMOUNT_1],
                                                                                [self.at2, AMOUNT_2]],
                                                packing_document_name="Foo")
        st = Stock.objects.all()
        art_1 = 0
        art_2 = 0
        for line in st:
            self.assertIsNone(line.label)
            if line.article == self.article_type:
                art_1 += 1
            elif line.article == self.at2:
                art_2 += 1
            else:
                self.assertTrue(False)
        self.assertEquals(art_1, 1)
        self.assertEquals(art_2, 1)
        self.assertEquals(len(st), 2)
        inv = Invoice.objects.all()
        self.assertEquals(len(inv), 0)

    def test_big_creation_function_stock_only_with_invoice(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        StockWish.create_stock_wish(user_modified=self.copro, articles_ordered=[[self.article_type, AMOUNT_1],
                                                                                [self.at2, AMOUNT_2]])
        SupplierOrder.create_supplier_order(self.copro, self.supplier,
                                            articles_ordered=[[self.article_type, AMOUNT_1, self.cost],
                                                              [self.at2, AMOUNT_2, self.cost]])
        PackingDocument.create_packing_document(user=self.copro, supplier=self.supplier,
                                                article_type_cost_combinations=[[self.article_type, AMOUNT_1,
                                                                                 self.cost2],[self.at2, AMOUNT_2]],
                                                packing_document_name="Foo", invoice_name="Bar")
        st = Stock.objects.all()
        art_1 = 0
        art_2 = 0
        for line in st:
            self.assertIsNone(line.label)
            if line.article == self.article_type:
                art_1 += 1
            elif line.article == self.at2:
                art_2 += 1
            else:
                self.assertTrue(False)
        self.assertEquals(art_1, 1)
        self.assertEquals(art_2, 1)
        self.assertEquals(len(st), 2)
        inv = Invoice.objects.all()
        self.assertEquals(len(inv), 1)

    def test_big_creation_function_mixed_no_invoice(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        StockWish.create_stock_wish(user_modified=self.copro, articles_ordered=[[self.article_type, AMOUNT_1-2],
                                                                                [self.at2, AMOUNT_2-2]])
        Order.create_order_from_wishables_combinations(user=self.copro, customer=self.customer,
                                                       wishable_type_number_price_combinations=[[self.article_type, 2,
                                                                                                 self.price],
                                                                                                [self.at2, 2,
                                                                                                 self.price]])
        SupplierOrder.create_supplier_order(self.copro, self.supplier,
                                            articles_ordered=[[self.article_type, AMOUNT_1, self.cost],
                                                              [self.at2, AMOUNT_2, self.cost]])
        PackingDocument.create_packing_document(user=self.copro, supplier=self.supplier,
                                                article_type_cost_combinations=[[self.article_type, AMOUNT_1],
                                                                                [self.at2, AMOUNT_2]],
                                                packing_document_name="Foo")
        st = Stock.objects.all()
        art_1 = 0
        art_2 = 0
        for line in st:
            if line.article == self.article_type:
                art_1 += 1
            elif line.article == self.at2:
                art_2 += 1
            else:
                self.assertTrue(False)
        self.assertEquals(art_1, 2)
        self.assertEquals(art_2, 2)
        self.assertEquals(len(st), 4)
        inv = Invoice.objects.all()
        self.assertEquals(len(inv), 0)

    def test_big_creation_function_mixed_with_invoice(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        StockWish.create_stock_wish(user_modified=self.copro, articles_ordered=[[self.article_type, AMOUNT_1-2],
                                                                                [self.at2, AMOUNT_2-2]])
        Order.create_order_from_wishables_combinations(user=self.copro, customer=self.customer,
                                                       wishable_type_number_price_combinations=[[self.article_type, 2,
                                                                                                 self.price],
                                                                                                [self.at2, 2,
                                                                                                 self.price]])
        SupplierOrder.create_supplier_order(self.copro, self.supplier,
                                            articles_ordered=[[self.article_type, AMOUNT_1, self.cost],
                                                              [self.at2, AMOUNT_2, self.cost]])
        PackingDocument.create_packing_document(user=self.copro, supplier=self.supplier,
                                                article_type_cost_combinations=[[self.article_type, AMOUNT_1,
                                                                                 self.cost2], [self.at2, AMOUNT_2]],
                                                packing_document_name="Foo", invoice_name="Bar")
        st = Stock.objects.all()
        art_1 = 0
        art_2 = 0
        for line in st:
            if line.article == self.article_type:
                art_1 += 1
            elif line.article == self.at2:
                art_2 += 1
            else:
                self.assertTrue(False)
        self.assertEquals(art_1, 2)
        self.assertEquals(art_2, 2)
        self.assertEquals(len(st), 4)
        inv = Invoice.objects.all()
        self.assertEquals(len(inv), 1)

    def test_serial_numbers_success(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        StockWish.create_stock_wish(user_modified=self.copro,
                                    articles_ordered=[[self.article_type, AMOUNT_1], [self.at2, AMOUNT_2]])
        SupplierOrder.create_supplier_order(self.copro, self.supplier,
                                            articles_ordered=[[self.article_type, AMOUNT_1, self.cost],
                                                              [self.at2, AMOUNT_2, self.cost]])
        sers = {self.article_type: ["ASD", "FD", "FDd", "FD", "GF", "Ga"], self.at2: ["Baz"]}
        PackingDocument.create_packing_document(user=self.copro, supplier=self.supplier,
                                                article_type_cost_combinations=[[self.article_type, AMOUNT_1],
                                                                                [self.at2, AMOUNT_2]],
                                                packing_document_name="Foo", serial_numbers=sers)
        sns = SerialNumber.objects.all()
        pac_doc = sns[0].packing_document
        counted_art_1 = 0
        counted_art_2 = 0
        for sn in sns:
            if sn.article_type == self.article_type and sn.packing_document == pac_doc:
                counted_art_1 += 1
            elif sn.article_type == self.at2 and sn.packing_document == pac_doc:
                counted_art_2 += 1
        self.assertEquals(counted_art_1, 6)
        self.assertEquals(counted_art_2, 1)

    def test_serial_numbers_fail(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        StockWish.create_stock_wish(user_modified=self.copro,
                                    articles_ordered=[[self.article_type, AMOUNT_1], [self.at2, AMOUNT_2]])
        SupplierOrder.create_supplier_order(self.copro, self.supplier,
                                            articles_ordered=[[self.article_type, AMOUNT_1, self.cost],
                                                              [self.at2, AMOUNT_2, self.cost]])
        sers = {self.article_type: ["ASD", "FD", "FDd", "FD", "GF", "Ga", "d"], self.at2: ["Baz"]}
        with self.assertRaises(IncorrectDataError):
            PackingDocument.create_packing_document(user=self.copro, supplier=self.supplier,
                                                    article_type_cost_combinations=[[self.article_type, AMOUNT_1],
                                                                                    [self.at2, AMOUNT_2]],
                                                    packing_document_name="Foo", serial_numbers=sers)

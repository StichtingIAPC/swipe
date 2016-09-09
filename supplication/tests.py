from django.test import TestCase
from decimal import Decimal
from money.models import VAT, AccountingGroup, Price, Currency, Cost, Money
from article.models import ArticleType
from crm.models import Person, User
from supplier.models import Supplier, ArticleTypeSupplier
from logistics.models import SupplierOrder
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

    def test_feature(self):
        FirstSupplierOrderStrategy.get_distribution([])

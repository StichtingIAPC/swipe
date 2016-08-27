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
        SupplierOrder.create_supplier_order(user=self.copro, supplier=self.supplier,
                                            articles_ordered=[[self.article_type, 1, self.cost]])
        pac_doc = PackingDocument(supplier=self.supplier, supplier_identifier="Foo", user=self.copro)
        pac_doc.save()
        sol = SupplierOrderLine.objects.get()
        pac_doc_line = PackingDocumentLine(article_type=self.article_type,
                                           packing_document=pac_doc, supplier_order_line=sol)
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
        SupplierOrder.create_supplier_order(user=self.copro, supplier=self.supplier,
                                            articles_ordered=[[self.article_type, 1, self.cost]])
        pac_doc = PackingDocument(supplier=self.supplier, supplier_identifier="Foo", user=self.copro)
        pac_doc.save()
        sol = SupplierOrderLine.objects.get()
        inv = Invoice(user=self.copro, supplier=self.supplier)
        inv.save()
        cost = Cost(amount=Decimal(2.78), use_system_currency=True)
        pac_doc_line = PackingDocumentLine(article_type=self.article_type,
                                           packing_document=pac_doc, supplier_order_line=sol,
                                           line_cost=cost, invoice=inv)
        pac_doc_line.save()
        assert pac_doc_line.invoice == inv
        assert pac_doc_line.line_cost == cost

    def test_illegal_article_type(self):
        order = Order(user_modified=self.copro, customer=self.customer)
        order.save()
        orderlines = []
        OrderLine.add_orderlines_to_list(orderlines, number=1, wishable_type=self.article_type,
                                         price=Price(amount=Decimal(1.55), currency=Currency("EUR")), user=self.copro)
        Order.make_order(order, orderlines, self.copro)
        SupplierOrder.create_supplier_order(user=self.copro, supplier=self.supplier,
                                            articles_ordered=[[self.article_type, 1, self.cost]])
        pac_doc = PackingDocument(supplier=self.supplier, supplier_identifier="Foo", user=self.copro)
        pac_doc.save()
        sol = SupplierOrderLine.objects.get()
        pac_doc_line = PackingDocumentLine(article_type=self.at2,
                                           packing_document=pac_doc, supplier_order_line=sol)
        caught = False
        try:
            pac_doc_line.save()
        except AssertionError:
            caught = True
        assert caught


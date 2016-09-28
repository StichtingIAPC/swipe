from django.test import TestCase
from article.tests import INeedSettings
from money.models import Currency, Cost, Money, VAT, Price, AccountingGroup
from register.models import SalesPeriod, InactiveError
from decimal import Decimal
from article.models import ArticleType, OtherCostType, AssortmentArticleBranch
from sales.models import SalesTransactionLine, Payment, Transaction, NotEnoughStockError, \
    OtherCostTransactionLine, OtherTransactionLine, TransactionLine, PaymentMisMatchError, NotEnoughOrderLinesError
from stock.models import Stock
from register.models import PaymentType
from crm.models import User, Person
from tools.util import _assert
from supplier.models import Supplier, ArticleTypeSupplier
from order.models import Order, OrderLine
from logistics.models import SupplierOrder, StockWish
from supplication.models import PackingDocument



class TestTransactionCreationFunction(INeedSettings, TestCase):

    def setUp(self):
        super().setUp()
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

        self.article_type = ArticleType(accounting_group=self.acc_group, name="Foo1", branch=self.branch)
        self.article_type.save()

        self.at2 = ArticleType(accounting_group=self.acc_group, name="Foo2", branch=self.branch)
        self.at2.save()

        self.at3 = ArticleType(accounting_group=self.acc_group, name="Foo3", branch=self.branch)
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

        self.pt = PaymentType.objects.create(name="Bla")
        self.pt2 = PaymentType.objects.create(name="Baz")

        self.cost = Cost(currency=Currency('EUR'), amount=Decimal(1.23))
        self.cost2 = Cost(currency=Currency('EUR'), amount=Decimal(1.24))

        self.simplest = SalesTransactionLine(article=self.article_type, count=1, cost=self.cost, price=self.price, num=1)
        self.simple_payment_usd = Payment(amount=self.money, payment_type=self.pt)
        self.simple_payment_eur = Payment(amount=Money(amount=Decimal(2.0), currency=Currency("EUR")),
                                          payment_type=self.pt)

        self.other_cost = OtherCostType(name="Oth1", branch=self.branch, accounting_group=self.acc_group,
                                        fixed_price=self.price
                                        )
        self.other_cost.save()

        self.sp = SalesPeriod.objects.create()


    def test_not_enough_stock_error(self):
        oalist = []
        oalist.append(SalesTransactionLine(price=self.price, count=1, order=None, article=self.article_type))
        caught = False
        try:
            Transaction.create_transaction(user=self.copro, payments=[self.simple_payment_usd], transaction_lines=oalist)
        except NotEnoughStockError:
            caught = True
        _assert(caught)

    def test_not_enough_parameters(self):

        caught = 0

        s1 = SalesTransactionLine(count=2, price=self.price)

        s2 = SalesTransactionLine(count=2, article=self.article_type)

        s3 = OtherCostTransactionLine(count=1, price=self.price)

        s4 = OtherCostTransactionLine(count=2, other_cost_type=self.other_cost)

        s5 = OtherTransactionLine(count=2, price=self.price)

        s6 = OtherTransactionLine(count=1, text="Bla")

        s7 = OtherTransactionLine(count=3, text="Bla", price=self.price)

        try:
            Transaction.create_transaction(user=self.copro, payments=[self.simple_payment_usd],
                                           transaction_lines=[s1])
        except AssertionError:
            caught += 1

        try:
            Transaction.create_transaction(user=self.copro, payments=[self.simple_payment_usd],
                                           transaction_lines=[s2])
        except AssertionError:
            caught += 1

        try:
            Transaction.create_transaction(user=self.copro, payments=[self.simple_payment_usd],
                                           transaction_lines=[s3])
        except AssertionError:
            caught += 1

        try:
            Transaction.create_transaction(user=self.copro, payments=[self.simple_payment_usd],
                                           transaction_lines=[s4])
        except AssertionError:
            caught += 1

        try:
            Transaction.create_transaction(user=self.copro, payments=[self.simple_payment_usd],
                                           transaction_lines=[s5])
        except AssertionError:
            caught += 1

        try:
            Transaction.create_transaction(user=self.copro, payments=[self.simple_payment_usd],
                                           transaction_lines=[s6])
        except AssertionError:
            caught += 1
        try:
            Transaction.create_transaction(user=self.copro, payments=[self.simple_payment_usd],
                                           transaction_lines=[s7])
        except AssertionError:
            caught += 1

        _assert(caught == 7)

    def test_sales_transaction_line_wrong_customer_stock(self):
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
        stl = SalesTransactionLine(price=Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True, vat=1.23),
                                   count=2, article=self.article_type)
        caught = False
        try:
            Transaction.create_transaction(user=self.copro, payments=[self.simple_payment_eur], transaction_lines=[stl])
        except NotEnoughStockError:
            caught = True
        _assert(caught)

    def test_sales_transaction_line(self):
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
        count = 2
        stl = SalesTransactionLine(price=Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True, vat=1.23),
                                   count=count, article=self.article_type, order=1)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount*count, currency=Currency("EUR"))
        local_payment=Payment(amount=loc_money, payment_type=self.pt)
        Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[stl])
        tls = TransactionLine.objects.all()
        _assert(len(tls) == 1)
        obj = tls[0]
        _assert(obj.num == 1)
        _assert(obj.count == 2)
        _assert(not obj.isRefunded)
        _assert(obj.order == 1)
        _assert(obj.text == str(self.article_type))
        st = Stock.objects.get(labeltype="Order", labelkey=1, article=self.article_type)
        _assert(st.count == AMOUNT_1-count)

    def test_sales_stock_level(self):
        AMOUNT_STOCK_1 = 5
        StockWish.create_stock_wish(user_modified=self.copro, articles_ordered=[(self.article_type, AMOUNT_STOCK_1)])
        SupplierOrder.create_supplier_order(supplier=self.supplier,
                                            articles_ordered=[[self.article_type, AMOUNT_STOCK_1, self.cost]],
                                            user_modified=self.copro)
        PackingDocument.create_packing_document(user=self.copro, supplier=self.supplier,
                                                article_type_cost_combinations=[[self.article_type, AMOUNT_STOCK_1]],
                                                packing_document_name="Foo")
        count = 3
        stl = SalesTransactionLine(
            price=Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True, vat=1.23),
            count=count, article=self.article_type, order=None)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount * count, currency=Currency("EUR"))
        local_payment = Payment(amount=loc_money, payment_type=self.pt)
        Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[stl])
        st = Stock.objects.get(labeltype__isnull=True, article=self.article_type)
        _assert(st.count == AMOUNT_STOCK_1-count)

    def test_sales_all_stock_levels(self):
        AMOUNT_STOCK_1 = 5
        AMOUNT_ORDER = 4
        Order.create_order_from_wishables_combinations(user=self.copro, customer=self.customer,
                                                       wishable_type_number_price_combinations=[[self.article_type, AMOUNT_ORDER, self.price]])
        StockWish.create_stock_wish(user_modified=self.copro, articles_ordered=[(self.article_type, AMOUNT_STOCK_1)])
        SupplierOrder.create_supplier_order(supplier=self.supplier,
                                            articles_ordered=[[self.article_type, AMOUNT_STOCK_1+AMOUNT_ORDER, self.cost]],
                                            user_modified=self.copro)
        PackingDocument.create_packing_document(user=self.copro, supplier=self.supplier,
                                                article_type_cost_combinations=[[self.article_type, AMOUNT_STOCK_1+AMOUNT_ORDER]],
                                                packing_document_name="Foo")
        count_stock = 3
        count_order = 2
        stl = SalesTransactionLine(
            price=Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True, vat=1.23),
            count=count_stock, article=self.article_type, order=None)
        stl2 = SalesTransactionLine(
            price=Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True, vat=1.23),
            count=count_order, article=self.article_type, order=1)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount * (count_stock+count_order), currency=Currency("EUR"))
        local_payment = Payment(amount=loc_money, payment_type=self.pt)
        Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[stl, stl2])
        st = Stock.objects.get(labeltype__isnull=True, article=self.article_type)
        _assert(st.count == AMOUNT_STOCK_1 - count_stock)
        st2 = Stock.objects.get(labeltype="Order", labelkey=1, article=self.article_type)
        _assert(st2.count == AMOUNT_ORDER-count_order)

    def test_sales_transaction_not_enough_stock(self):
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
        count = AMOUNT_1+1
        stl = SalesTransactionLine(price=Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True, vat=1.23),
                                   count=count, article=self.article_type, order=1)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount*count, currency=Currency("EUR"))
        local_payment=Payment(amount=loc_money, payment_type=self.pt)
        caught = False
        try:
            Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[stl])
        except NotEnoughStockError:
            caught = True
        _assert(caught)

    def test_sales_transaction_just_enough_stock(self):
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
        count = AMOUNT_1
        stl = SalesTransactionLine(price=Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True, vat=1.23),
                                   count=count, article=self.article_type, order=1)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount*count, currency=Currency("EUR"))
        local_payment=Payment(amount=loc_money, payment_type=self.pt)

        Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[stl])

    def test_sales_transaction_too_much_payment(self):
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
        count = AMOUNT_1
        stl = SalesTransactionLine(price=Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True, vat=1.23),
                                   count=count, article=self.article_type, order=1)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount*count+Decimal(0.001), currency=Currency("EUR"))
        local_payment=Payment(amount=loc_money, payment_type=self.pt)
        caught = False
        try:
            Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[stl])
        except PaymentMisMatchError:
            caught = True
        _assert(caught)

    def test_sales_transaction_too_little_payment(self):
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
        count = AMOUNT_1
        stl = SalesTransactionLine(price=Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True, vat=1.23),
                                   count=count, article=self.article_type, order=1)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount*count-Decimal(0.001), currency=Currency("EUR"))
        local_payment=Payment(amount=loc_money, payment_type=self.pt)
        caught = False
        try:
            Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[stl])
        except PaymentMisMatchError:
            caught = True
        _assert(caught)

    def test_sales_transaction_other_cost(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        AMOUNT_3 = 5
        Order.create_order_from_wishables_combinations(self.copro, self.customer,
                                                       [[self.article_type, AMOUNT_1, self.price],
                                                        [self.at2, AMOUNT_2, self.price],[self.other_cost, AMOUNT_3, self.price]])
        SupplierOrder.create_supplier_order(self.copro, self.supplier,
                                            articles_ordered=[[self.article_type, AMOUNT_1, self.cost],
                                                              [self.at2, AMOUNT_2, self.cost]])
        PackingDocument.create_packing_document(user=self.copro, supplier=self.supplier,
                                                article_type_cost_combinations=[[self.article_type, AMOUNT_1],
                                                                                [self.at2, AMOUNT_2]],
                                                packing_document_name="Foo")
        count = AMOUNT_3-1
        octt = OtherCostTransactionLine(price=Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True, vat=1.23),
                                        count=count, other_cost_type=self.other_cost, order=1)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount*count, currency=Currency("EUR"))
        local_payment=Payment(amount=loc_money, payment_type=self.pt)
        Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[octt])
        tls = TransactionLine.objects.all()
        _assert(len(tls) == 1)
        octls = OtherCostTransactionLine.objects.all()
        _assert(len(octls) == 1)
        octl= octls[0]
        _assert(not octl.isRefunded)
        _assert(octl.count == count)
        _assert(octl.order == 1)
        _assert(octl.text == octl.other_cost_type.name)
        sold_counter = 0
        ols = OrderLine.objects.filter(wishable__sellabletype=self.other_cost, order_id=1)
        for ol in ols:
            if ol.state == 'S':
                sold_counter += 1
        _assert(sold_counter == count)

    def test_sales_transaction_other_cost_just_enough_orderlines(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        AMOUNT_3 = 5
        Order.create_order_from_wishables_combinations(self.copro, self.customer,
                                                       [[self.article_type, AMOUNT_1, self.price],
                                                        [self.at2, AMOUNT_2, self.price],[self.other_cost, AMOUNT_3, self.price]])
        SupplierOrder.create_supplier_order(self.copro, self.supplier,
                                            articles_ordered=[[self.article_type, AMOUNT_1, self.cost],
                                                              [self.at2, AMOUNT_2, self.cost]])
        PackingDocument.create_packing_document(user=self.copro, supplier=self.supplier,
                                                article_type_cost_combinations=[[self.article_type, AMOUNT_1],
                                                                                [self.at2, AMOUNT_2]],
                                                packing_document_name="Foo")
        count = AMOUNT_3
        octt = OtherCostTransactionLine(price=Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True, vat=1.23),
                                        count=count, other_cost_type=self.other_cost, order=1)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount*count, currency=Currency("EUR"))
        local_payment=Payment(amount=loc_money, payment_type=self.pt)
        Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[octt])
        tls = TransactionLine.objects.all()
        _assert(len(tls) == 1)
        octls = OtherCostTransactionLine.objects.all()
        _assert(len(octls) == 1)
        octl= octls[0]
        _assert(not octl.isRefunded)
        _assert(octl.count == count)
        _assert(octl.order == 1)
        _assert(octl.text == octl.other_cost_type.name)
        sold_counter = 0
        ols = OrderLine.objects.filter(wishable__sellabletype=self.other_cost, order_id=1)
        for ol in ols:
            if ol.state == 'S':
                sold_counter += 1
        _assert(sold_counter == count)

    def test_sales_transaction_other_cost_not_enough_orderlines(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        AMOUNT_3 = 5
        Order.create_order_from_wishables_combinations(self.copro, self.customer,
                                                       [[self.article_type, AMOUNT_1, self.price],
                                                        [self.at2, AMOUNT_2, self.price],[self.other_cost, AMOUNT_3, self.price]])
        SupplierOrder.create_supplier_order(self.copro, self.supplier,
                                            articles_ordered=[[self.article_type, AMOUNT_1, self.cost],
                                                              [self.at2, AMOUNT_2, self.cost]])
        PackingDocument.create_packing_document(user=self.copro, supplier=self.supplier,
                                                article_type_cost_combinations=[[self.article_type, AMOUNT_1],
                                                                                [self.at2, AMOUNT_2]],
                                                packing_document_name="Foo")
        count = AMOUNT_3+1
        octt = OtherCostTransactionLine(price=Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True, vat=1.23),
                                        count=count, other_cost_type=self.other_cost, order=1)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount*count, currency=Currency("EUR"))
        local_payment=Payment(amount=loc_money, payment_type=self.pt)
        caught = False
        try:
            Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[octt])
        except NotEnoughOrderLinesError:
            caught = True
        _assert(caught)

    def test_sales_transaction_other_line(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        AMOUNT_3 = 5
        Order.create_order_from_wishables_combinations(self.copro, self.customer,
                                                       [[self.article_type, AMOUNT_1, self.price],
                                                        [self.at2, AMOUNT_2, self.price],[self.other_cost, AMOUNT_3, self.price]])
        SupplierOrder.create_supplier_order(self.copro, self.supplier,
                                            articles_ordered=[[self.article_type, AMOUNT_1, self.cost],
                                                              [self.at2, AMOUNT_2, self.cost]])
        PackingDocument.create_packing_document(user=self.copro, supplier=self.supplier,
                                                article_type_cost_combinations=[[self.article_type, AMOUNT_1],
                                                                                [self.at2, AMOUNT_2]],
                                                packing_document_name="Foo")
        count = 10
        p = Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True, vat=1.23)
        otl = OtherTransactionLine(count=count, price=p, text="Meh", accounting_group=self.acc_group)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount*count, currency=Currency("EUR"))
        local_payment = Payment(amount=loc_money, payment_type=self.pt)
        Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[otl])
        tl = TransactionLine.objects.get()
        otl = OtherTransactionLine.objects.get()
        _assert(otl.count == count)
        _assert(not otl.isRefunded)
        _assert(otl.text == "Meh")
        _assert(otl.num == -1)

    def test_sales_transaction_wrong_currency(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        AMOUNT_3 = 5
        Order.create_order_from_wishables_combinations(self.copro, self.customer,
                                                       [[self.article_type, AMOUNT_1, self.price],
                                                        [self.at2, AMOUNT_2, self.price],[self.other_cost, AMOUNT_3, self.price]])
        SupplierOrder.create_supplier_order(self.copro, self.supplier,
                                            articles_ordered=[[self.article_type, AMOUNT_1, self.cost],
                                                              [self.at2, AMOUNT_2, self.cost]])
        PackingDocument.create_packing_document(user=self.copro, supplier=self.supplier,
                                                article_type_cost_combinations=[[self.article_type, AMOUNT_1],
                                                                                [self.at2, AMOUNT_2]],
                                                packing_document_name="Foo")
        count = 10
        p = Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True, vat=1.23)
        otl = OtherTransactionLine(count=count, price=p, text="Meh", accounting_group=self.acc_group)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount*count, currency=Currency("USD"))
        local_payment = Payment(amount=loc_money, payment_type=self.pt)
        caught = False
        try:
            Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[otl])
        except PaymentMisMatchError:
            caught = True
        _assert(caught)

    def test_sales_transaction_two_payments(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        AMOUNT_3 = 5
        Order.create_order_from_wishables_combinations(self.copro, self.customer,
                                                       [[self.article_type, AMOUNT_1, self.price],
                                                        [self.at2, AMOUNT_2, self.price],[self.other_cost, AMOUNT_3, self.price]])
        SupplierOrder.create_supplier_order(self.copro, self.supplier,
                                            articles_ordered=[[self.article_type, AMOUNT_1, self.cost],
                                                              [self.at2, AMOUNT_2, self.cost]])
        PackingDocument.create_packing_document(user=self.copro, supplier=self.supplier,
                                                article_type_cost_combinations=[[self.article_type, AMOUNT_1],
                                                                                [self.at2, AMOUNT_2]],
                                                packing_document_name="Foo")
        count = 10
        p = Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True, vat=1.23)
        otl = OtherTransactionLine(count=count, price=p, text="Meh", accounting_group=self.acc_group)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount*count-Decimal(1), currency=Currency("EUR"))
        local_payment = Payment(amount=loc_money, payment_type=self.pt)
        local_payment2 = Payment(amount=Money(amount=Decimal(1), currency=Currency("EUR")), payment_type=self.pt2)
        Transaction.create_transaction(user=self.copro, payments=[local_payment, local_payment2], transaction_lines=[otl])

    def test_sales_transaction_mixed_transaction_lines(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        AMOUNT_3 = 5
        Order.create_order_from_wishables_combinations(self.copro, self.customer,
                                                       [[self.article_type, AMOUNT_1, self.price],
                                                        [self.at2, AMOUNT_2, self.price],[self.other_cost, AMOUNT_3, self.price]])
        SupplierOrder.create_supplier_order(self.copro, self.supplier,
                                            articles_ordered=[[self.article_type, AMOUNT_1, self.cost],
                                                              [self.at2, AMOUNT_2, self.cost]])
        PackingDocument.create_packing_document(user=self.copro, supplier=self.supplier,
                                                article_type_cost_combinations=[[self.article_type, AMOUNT_1],
                                                                                [self.at2, AMOUNT_2]],
                                                packing_document_name="Foo")
        count_1 = AMOUNT_1-4
        count_2 = AMOUNT_2-2
        count_3 = AMOUNT_3-2
        count_4 = 10
        total_count=count_1+count_2+count_3+count_4
        p = Price(amount=Decimal(1), use_system_currency=True, vat=1.23)
        stl_1 = SalesTransactionLine(count=count_1, price=p, article=self.article_type, order=1)
        stl_2 = SalesTransactionLine(count=count_2, price=p, article=self.at2, order=1)
        octl = OtherCostTransactionLine(count=count_3, price=p, other_cost_type=self.other_cost)
        otl = OtherTransactionLine(count=count_4, price=p, text="Rand", accounting_group=self.acc_group)
        loc_money = Money(amount=Decimal(1)*total_count-Decimal(1), currency=Currency("EUR"))
        local_payment = Payment(amount=loc_money, payment_type=self.pt)
        local_payment2 = Payment(amount=Money(amount=Decimal(1), currency=Currency("EUR")), payment_type=self.pt2)
        Transaction.create_transaction(user=self.copro, payments=[local_payment, local_payment2], transaction_lines=[stl_1, stl_2, octl, otl])
        tls = TransactionLine.objects.all()
        _assert(len(tls) == 4)
        stls = SalesTransactionLine.objects.all()
        _assert(len(stls) == 2)
        OtherCostTransactionLine.objects.get()
        OtherTransactionLine.objects.get()
        pmnts = Payment.objects.all()
        _assert(len(pmnts) == 2)
        Transaction.objects.get()







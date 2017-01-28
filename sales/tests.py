from decimal import Decimal

from django.test import TestCase
from tools.testing import TestData
from swipe.settings import USED_CURRENCY

from article.models import ArticleType, OtherCostType
from article.tests import INeedSettings
from crm.models import User, Person
from logistics.models import SupplierOrder, StockWish
from money.models import Currency, Cost, Money, VAT, Price, AccountingGroup, CurrencyData
from order.models import Order, OrderLine
from register.models import PaymentType, Register
from sales import models
from sales.models import SalesTransactionLine, Payment, Transaction, NotEnoughStockError, \
    OtherCostTransactionLine, OtherTransactionLine, TransactionLine, PaymentMisMatchError, NotEnoughOrderLinesError, \
    PaymentTypeError, RefundTransactionLine, RefundError, InvalidDataException
from stock.models import Stock
from supplication.models import PackingDocument
from supplier.models import Supplier, ArticleTypeSupplier


class TestTransactionCreationFunction(INeedSettings, TestCase, TestData):

    def setUp(self):
        super().setUp()
        self.part_setup_vat_group()
        self.vat_group = self.vat_group_high
        self.price = Price(amount=Decimal("1.00"), use_system_currency=True)
        self.currency = Currency(iso=USED_CURRENCY)

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
        self.pt3 = PaymentType.objects.create(name="Quux")

        self.cost = Cost(currency=Currency(USED_CURRENCY), amount=Decimal(1.23))
        self.cost2 = Cost(currency=Currency(USED_CURRENCY), amount=Decimal(1.24))

        self.simplest = SalesTransactionLine(article=self.article_type, count=1, cost=self.cost,
                                             price=self.price, num=1)
        self.simple_payment_usd = Payment(amount=self.money, payment_type=self.pt)
        self.simple_payment_eur = Payment(amount=Money(amount=Decimal(2.0), currency=Currency(USED_CURRENCY)),
                                          payment_type=self.pt)

        self.other_cost = OtherCostType(name="Oth1", branch=self.branch, accounting_group=self.acc_group,
                                        fixed_price=self.price
                                        )
        self.other_cost.save()
        self.currency_data_eur = CurrencyData(iso="EUR", name="Euro", symbol="€", digits=2)
        self.currency_data_eur.save()

        self.register = Register(currency=self.currency_data_eur, name="Foo", is_cash_register=False, is_active=True,
                                 payment_type=self.pt)
        self.register.save()
        self.register2 = Register(currency=self.currency_data_eur, name="Bar", is_cash_register=False, is_active=True,
                                  payment_type=self.pt2)
        self.register2.save()
        self.register.open(counted_amount=Decimal(0))
        self.register2.open(counted_amount=Decimal(0))

    def test_not_enough_stock_error(self):
        oalist = [SalesTransactionLine(price=self.price, count=1, order=None, article=self.article_type)]
        with self.assertRaises(NotEnoughStockError):
            Transaction.create_transaction(user=self.copro, payments=[self.simple_payment_usd],
                                           transaction_lines=oalist)

    def test_not_enough_parameters(self):
        s1 = SalesTransactionLine(count=2, price=self.price)

        s2 = SalesTransactionLine(count=2, article=self.article_type)

        s3 = OtherCostTransactionLine(count=1, price=self.price)

        s4 = OtherCostTransactionLine(count=2, other_cost_type=self.other_cost)

        s5 = OtherTransactionLine(count=2, price=self.price)

        s6 = OtherTransactionLine(count=1, text="Bla")

        s7 = OtherTransactionLine(count=3, text="Bla", price=self.price)

        with self.assertRaises(models.InvalidDataException):
            Transaction.create_transaction(user=self.copro, payments=[self.simple_payment_usd],
                                           transaction_lines=[s1])
        with self.assertRaises(models.IncorrectDataException):
            Transaction.create_transaction(user=self.copro, payments=[self.simple_payment_usd],
                                           transaction_lines=[s2])
        with self.assertRaises(models.InvalidDataException):
            Transaction.create_transaction(user=self.copro, payments=[self.simple_payment_usd],
                                           transaction_lines=[s3])
        with self.assertRaises(models.IncorrectDataException):
            Transaction.create_transaction(user=self.copro, payments=[self.simple_payment_usd],
                                           transaction_lines=[s4])
        with self.assertRaises(models.IncorrectDataException):
            Transaction.create_transaction(user=self.copro, payments=[self.simple_payment_usd],
                                           transaction_lines=[s5])
        with self.assertRaises(models.IncorrectDataException):
            Transaction.create_transaction(user=self.copro, payments=[self.simple_payment_usd],
                                           transaction_lines=[s6])
        with self.assertRaises(models.InvalidDataException):
            Transaction.create_transaction(user=self.copro, payments=[self.simple_payment_usd],
                                           transaction_lines=[s7])

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
        stl = SalesTransactionLine(price=Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True,
                                               vat=1.23),
                                   count=2, article=self.article_type)
        with self.assertRaises(NotEnoughStockError):
            Transaction.create_transaction(user=self.copro, payments=[self.simple_payment_eur], transaction_lines=[stl])

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
        stl = SalesTransactionLine(price=Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True,
                                               vat=1.23),
                                   count=count, article=self.article_type, order=1)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount*count, currency=Currency(USED_CURRENCY))
        local_payment=Payment(amount=loc_money, payment_type=self.pt)
        Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[stl])
        tls = TransactionLine.objects.all()
        self.assertEquals(len(tls), 1)
        obj = tls[0]
        self.assertEquals(obj.num, 1)
        self.assertEquals(obj.count, 2)
        self.assertFalse(obj.isRefunded)
        self.assertEquals(obj.order, 1)
        self.assertEquals(obj.text, str(self.article_type))
        st = Stock.objects.get(labeltype="Order", labelkey=1, article=self.article_type)
        self.assertEquals(st.count, AMOUNT_1-count)
        ols_1 = OrderLine.objects.filter(wishable__sellabletype=self.article_type, state='S')
        ols_2 = OrderLine.objects.filter(wishable__sellabletype=self.article_type, state='A')
        ols = OrderLine.objects.filter(wishable__sellabletype=self.article_type)
        self.assertEquals(len(ols_1), count)
        self.assertEquals(len(ols_2), AMOUNT_1-count)

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
        loc_money = Money(amount=self.simple_payment_eur.amount.amount * count, currency=Currency(USED_CURRENCY))
        local_payment = Payment(amount=loc_money, payment_type=self.pt)
        Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[stl])
        st = Stock.objects.get(labeltype__isnull=True, article=self.article_type)
        self.assertEquals(st.count, AMOUNT_STOCK_1-count)

    def test_sales_all_stock_levels(self):
        AMOUNT_STOCK_1 = 5
        AMOUNT_ORDER = 4
        Order.create_order_from_wishables_combinations(user=self.copro, customer=self.customer,
                                                       wishable_type_number_price_combinations=[[self.article_type,
                                                                                                 AMOUNT_ORDER,
                                                                                                 self.price]])
        StockWish.create_stock_wish(user_modified=self.copro, articles_ordered=[(self.article_type, AMOUNT_STOCK_1)])
        SupplierOrder.create_supplier_order(supplier=self.supplier,
                                            articles_ordered=[[self.article_type, AMOUNT_STOCK_1+AMOUNT_ORDER,
                                                               self.cost]],
                                            user_modified=self.copro)
        PackingDocument.create_packing_document(user=self.copro, supplier=self.supplier,
                                                article_type_cost_combinations=[[self.article_type,
                                                                                 AMOUNT_STOCK_1+AMOUNT_ORDER]],
                                                packing_document_name="Foo")
        count_stock = 3
        count_order = 2
        stl = SalesTransactionLine(
            price=Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True, vat=1.23),
            count=count_stock, article=self.article_type, order=None)
        stl2 = SalesTransactionLine(
            price=Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True, vat=1.23),
            count=count_order, article=self.article_type, order=1)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount * (count_stock+count_order),
                          currency=Currency(USED_CURRENCY))
        local_payment = Payment(amount=loc_money, payment_type=self.pt)
        Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[stl, stl2])
        st = Stock.objects.get(labeltype__isnull=True, article=self.article_type)
        self.assertEquals(st.count, AMOUNT_STOCK_1 - count_stock)
        st2 = Stock.objects.get(labeltype="Order", labelkey=1, article=self.article_type)
        self.assertEquals(st2.count, AMOUNT_ORDER-count_order)

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
        stl = SalesTransactionLine(price=Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True,
                                               vat=1.23),
                                   count=count, article=self.article_type, order=1)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount*count, currency=Currency(USED_CURRENCY))
        local_payment=Payment(amount=loc_money, payment_type=self.pt)
        with self.assertRaises(NotEnoughStockError):
            Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[stl])

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
        stl = SalesTransactionLine(price=Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True,
                                               vat=1.23),
                                   count=count, article=self.article_type, order=1)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount*count, currency=Currency(USED_CURRENCY))
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
        stl = SalesTransactionLine(price=Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True,
                                               vat=1.23),
                                   count=count, article=self.article_type, order=1)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount*count+Decimal(0.001), currency=Currency(USED_CURRENCY))
        local_payment=Payment(amount=loc_money, payment_type=self.pt)

        with self.assertRaises(PaymentMisMatchError):
            Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[stl])

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
        stl = SalesTransactionLine(price=Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True,
                                               vat=1.23),
                                   count=count, article=self.article_type, order=1)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount*count-Decimal(0.001), currency=Currency(USED_CURRENCY))
        local_payment=Payment(amount=loc_money, payment_type=self.pt)
        with self.assertRaises(PaymentMisMatchError):
            Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[stl])

    def test_sales_transaction_other_cost(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        AMOUNT_3 = 5
        Order.create_order_from_wishables_combinations(self.copro, self.customer,
                                                       [[self.article_type, AMOUNT_1, self.price],
                                                        [self.at2, AMOUNT_2, self.price], [self.other_cost, AMOUNT_3,
                                                                                          self.price]])
        SupplierOrder.create_supplier_order(self.copro, self.supplier,
                                            articles_ordered=[[self.article_type, AMOUNT_1, self.cost],
                                                              [self.at2, AMOUNT_2, self.cost]])
        PackingDocument.create_packing_document(user=self.copro, supplier=self.supplier,
                                                article_type_cost_combinations=[[self.article_type, AMOUNT_1],
                                                                                [self.at2, AMOUNT_2]],
                                                packing_document_name="Foo")
        count = AMOUNT_3-1
        octt = OtherCostTransactionLine(price=Price(amount=self.simple_payment_eur.amount.amount,
                                                    use_system_currency=True, vat=1.23),
                                        count=count, other_cost_type=self.other_cost, order=1)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount*count, currency=Currency(USED_CURRENCY))
        local_payment=Payment(amount=loc_money, payment_type=self.pt)
        Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[octt])
        tls = TransactionLine.objects.all()
        self.assertEquals(len(tls), 1)
        octls = OtherCostTransactionLine.objects.all()
        self.assertEquals(len(octls), 1)
        octl= octls[0]
        self.assertFalse(octl.isRefunded)
        self.assertEquals(octl.count, count)
        self.assertEquals(octl.order, 1)
        self.assertEquals(octl.text, octl.other_cost_type.name)
        sold_counter = 0
        ols = OrderLine.objects.filter(wishable__sellabletype=self.other_cost, order_id=1)
        for ol in ols:
            if ol.state == 'S':
                sold_counter += 1
        self.assertEquals(sold_counter, count)

    def test_sales_transaction_other_cost_just_enough_orderlines(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        AMOUNT_3 = 5
        Order.create_order_from_wishables_combinations(self.copro, self.customer,
                                                       [[self.article_type, AMOUNT_1, self.price],
                                                        [self.at2, AMOUNT_2, self.price], [self.other_cost, AMOUNT_3,
                                                                                           self.price]])
        SupplierOrder.create_supplier_order(self.copro, self.supplier,
                                            articles_ordered=[[self.article_type, AMOUNT_1, self.cost],
                                                              [self.at2, AMOUNT_2, self.cost]])
        PackingDocument.create_packing_document(user=self.copro, supplier=self.supplier,
                                                article_type_cost_combinations=[[self.article_type, AMOUNT_1],
                                                                                [self.at2, AMOUNT_2]],
                                                packing_document_name="Foo")
        count = AMOUNT_3
        octt = OtherCostTransactionLine(price=Price(amount=self.simple_payment_eur.amount.amount,
                                                    use_system_currency=True, vat=1.23),
                                        count=count, other_cost_type=self.other_cost, order=1)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount*count, currency=Currency(USED_CURRENCY))
        local_payment=Payment(amount=loc_money, payment_type=self.pt)
        Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[octt])
        tls = TransactionLine.objects.all()
        self.assertEquals(len(tls), 1)
        octls = OtherCostTransactionLine.objects.all()
        self.assertEquals(len(octls), 1)
        octl= octls[0]
        self.assertFalse(octl.isRefunded)
        self.assertEquals(octl.count, count)
        self.assertEquals(octl.order, 1)
        self.assertEquals(octl.text, octl.other_cost_type.name)
        sold_counter = 0
        ols = OrderLine.objects.filter(wishable__sellabletype=self.other_cost, order_id=1)
        for ol in ols:
            if ol.state == 'S':
                sold_counter += 1
        self.assertEquals(sold_counter, count)

    def test_sales_transaction_other_cost_not_enough_orderlines(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        AMOUNT_3 = 5
        Order.create_order_from_wishables_combinations(self.copro, self.customer,
                                                       [[self.article_type, AMOUNT_1, self.price],
                                                        [self.at2, AMOUNT_2, self.price], [self.other_cost, AMOUNT_3,
                                                                                           self.price]])
        SupplierOrder.create_supplier_order(self.copro, self.supplier,
                                            articles_ordered=[[self.article_type, AMOUNT_1, self.cost],
                                                              [self.at2, AMOUNT_2, self.cost]])
        PackingDocument.create_packing_document(user=self.copro, supplier=self.supplier,
                                                article_type_cost_combinations=[[self.article_type, AMOUNT_1],
                                                                                [self.at2, AMOUNT_2]],
                                                packing_document_name="Foo")
        count = AMOUNT_3+1
        octt = OtherCostTransactionLine(price=Price(amount=self.simple_payment_eur.amount.amount,
                                                    use_system_currency=True, vat=1.23),
                                        count=count, other_cost_type=self.other_cost, order=1)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount*count, currency=Currency(USED_CURRENCY))
        local_payment=Payment(amount=loc_money, payment_type=self.pt)
        with self.assertRaises(NotEnoughOrderLinesError):
            Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[octt])

    def test_sales_transaction_other_line(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        AMOUNT_3 = 5
        Order.create_order_from_wishables_combinations(self.copro, self.customer,
                                                       [[self.article_type, AMOUNT_1, self.price],
                                                        [self.at2, AMOUNT_2, self.price], [self.other_cost, AMOUNT_3,
                                                                                           self.price]])
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
        loc_money = Money(amount=self.simple_payment_eur.amount.amount*count, currency=Currency(USED_CURRENCY))
        local_payment = Payment(amount=loc_money, payment_type=self.pt)
        Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[otl])
        tl = TransactionLine.objects.get()
        otl = OtherTransactionLine.objects.get()
        self.assertEquals(otl.count, count)
        self.assertFalse(otl.isRefunded)
        self.assertEquals(otl.text, "Meh")
        self.assertEquals(otl.num, -1)

    def test_sales_transaction_wrong_currency(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        AMOUNT_3 = 5
        Order.create_order_from_wishables_combinations(self.copro, self.customer,
                                                       [[self.article_type, AMOUNT_1, self.price],
                                                        [self.at2, AMOUNT_2, self.price], [self.other_cost, AMOUNT_3,
                                                                                           self.price]])
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
        with self.assertRaises(InvalidDataException):
            Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[otl])

    def test_sales_transaction_two_payments(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        AMOUNT_3 = 5
        Order.create_order_from_wishables_combinations(self.copro, self.customer,
                                                       [[self.article_type, AMOUNT_1, self.price],
                                                        [self.at2, AMOUNT_2, self.price], [self.other_cost, AMOUNT_3,
                                                                                           self.price]])
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
        loc_money = Money(amount=self.simple_payment_eur.amount.amount*count-Decimal(1), currency=Currency(USED_CURRENCY))
        local_payment = Payment(amount=loc_money, payment_type=self.pt)
        local_payment2 = Payment(amount=Money(amount=Decimal(1), currency=Currency(USED_CURRENCY)), payment_type=self.pt2)
        Transaction.create_transaction(user=self.copro, payments=[local_payment, local_payment2],
                                       transaction_lines=[otl])

    def test_sales_transaction_mixed_transaction_lines(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        AMOUNT_3 = 5
        Order.create_order_from_wishables_combinations(self.copro, self.customer,
                                                       [[self.article_type, AMOUNT_1, self.price],
                                                        [self.at2, AMOUNT_2, self.price], [self.other_cost, AMOUNT_3,
                                                                                           self.price]])
        SupplierOrder.create_supplier_order(self.copro, self.supplier,
                                            articles_ordered=[[self.article_type, AMOUNT_1, self.cost],
                                                              [self.at2, AMOUNT_2, self.cost]])
        PackingDocument.create_packing_document(user=self.copro, supplier=self.supplier,
                                                article_type_cost_combinations=[[self.article_type, AMOUNT_1],
                                                                                [self.at2, AMOUNT_2]],
                                                packing_document_name="Foo")
        count_1 = AMOUNT_1 - 4
        count_2 = AMOUNT_2 - 2
        count_3 = AMOUNT_3 - 2
        count_4 = 10
        total_count = count_1 + count_2 + count_3 + count_4
        p = Price(amount=Decimal(1), use_system_currency=True, vat=1.23)
        stl_1 = SalesTransactionLine(count=count_1, price=p, article=self.article_type, order=1)
        stl_2 = SalesTransactionLine(count=count_2, price=p, article=self.at2, order=1)
        octl = OtherCostTransactionLine(count=count_3, price=p, other_cost_type=self.other_cost)
        otl = OtherTransactionLine(count=count_4, price=p, text="Rand", accounting_group=self.acc_group)
        loc_money = Money(amount=Decimal(1)*total_count-Decimal(1), currency=Currency(USED_CURRENCY))
        local_payment = Payment(amount=loc_money, payment_type=self.pt)
        local_payment2 = Payment(amount=Money(amount=Decimal(1), currency=Currency(USED_CURRENCY)), payment_type=self.pt2)
        Transaction.create_transaction(user=self.copro, payments=[local_payment, local_payment2],
                                       transaction_lines=[stl_1, stl_2, octl, otl])
        tls = TransactionLine.objects.all()
        self.assertEquals(len(tls), 4)
        stls = SalesTransactionLine.objects.all()
        self.assertEquals(len(stls), 2)
        OtherCostTransactionLine.objects.get()
        OtherTransactionLine.objects.get()
        pmnts = Payment.objects.all()
        self.assertEquals(len(pmnts), 2)
        Transaction.objects.get()

    def test_transaction_payment_not_in_opened_register(self):
        count = 2
        p = Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True, vat=1.23)
        otl = OtherTransactionLine(count=count, price=p, text="Meh", accounting_group=self.acc_group)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount * count, currency=Currency(USED_CURRENCY))
        local_payment = Payment(amount=loc_money, payment_type=self.pt3)
        with self.assertRaises(PaymentTypeError):
            Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[otl])

    def test_refund_line(self):
        count = 5
        p = Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True, vat=1.23)
        otl = OtherTransactionLine(count=count, price=p, text="Meh", accounting_group=self.acc_group)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount * count, currency=Currency(USED_CURRENCY))
        local_payment = Payment(amount=loc_money, payment_type=self.pt)
        Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[otl])
        count_refund = -2
        trl = TransactionLine.objects.get()
        rfl = RefundTransactionLine(count=count_refund, price=p, sold_transaction_line=trl)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount * count_refund, currency=Currency(USED_CURRENCY))
        nega_payment = Payment(amount=loc_money, payment_type=self.pt)
        Transaction.create_transaction(user=self.copro, payments=[nega_payment], transaction_lines=[rfl])
        trls = TransactionLine.objects.all()
        self.assertEquals(len(trls), 2)
        self.assertIsNone(trls[1].order)
        self.assertEquals(trls[1].num, -1)
        self.assertEquals(trls[1].count, count_refund)
        self.assertEquals(trls[1].text, trls[0].text)

    def test_refund_line_too_many_refunded(self):
        count = 5
        p = Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True, vat=1.23)
        otl = OtherTransactionLine(count=count, price=p, text="Meh", accounting_group=self.acc_group)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount * count, currency=Currency(USED_CURRENCY))
        local_payment = Payment(amount=loc_money, payment_type=self.pt)
        Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[otl])
        count_refund = -6
        trl = TransactionLine.objects.get()
        rfl = RefundTransactionLine(count=count_refund, price=p, sold_transaction_line=trl)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount * count_refund, currency=Currency(USED_CURRENCY))
        nega_payment = Payment(amount=loc_money, payment_type=self.pt)
        with self.assertRaises(RefundError):
            Transaction.create_transaction(user=self.copro, payments=[nega_payment], transaction_lines=[rfl])

    def test_refund_line_just_enough_refunded(self):
        count = 5
        p = Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True, vat=1.23)
        otl = OtherTransactionLine(count=count, price=p, text="Meh", accounting_group=self.acc_group)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount * count, currency=Currency(USED_CURRENCY))
        local_payment = Payment(amount=loc_money, payment_type=self.pt)
        Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[otl])
        count_refund = -5
        trl = TransactionLine.objects.get()
        rfl = RefundTransactionLine(count=count_refund, price=p, sold_transaction_line=trl)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount * count_refund, currency=Currency(USED_CURRENCY))
        nega_payment = Payment(amount=loc_money, payment_type=self.pt)
        Transaction.create_transaction(user=self.copro, payments=[nega_payment], transaction_lines=[rfl])

    def test_refund_line_too_many_refunded_two_new_refunds(self):
        count = 5
        p = Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True, vat=1.23)
        otl = OtherTransactionLine(count=count, price=p, text="Meh", accounting_group=self.acc_group)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount * count, currency=Currency(USED_CURRENCY))
        local_payment = Payment(amount=loc_money, payment_type=self.pt)
        Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[otl])
        count_refund_1 = -3
        count_refund_2 = -3
        count_refund_total = count_refund_1 + count_refund_2
        trl = TransactionLine.objects.get()
        rfl = RefundTransactionLine(count=count_refund_1, price=p, sold_transaction_line=trl)
        rfl2 = RefundTransactionLine(count=count_refund_2, price=p, sold_transaction_line=trl)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount * count_refund_total, currency=Currency(USED_CURRENCY))
        nega_payment = Payment(amount=loc_money, payment_type=self.pt)
        with self.assertRaises(RefundError):
            Transaction.create_transaction(user=self.copro, payments=[nega_payment], transaction_lines=[rfl, rfl2])

    def test_refund_line_too_many_old_new_refunded(self):
        count = 5
        p = Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True, vat=1.23)
        otl = OtherTransactionLine(count=count, price=p, text="Meh", accounting_group=self.acc_group)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount * count, currency=Currency(USED_CURRENCY))
        local_payment = Payment(amount=loc_money, payment_type=self.pt)
        Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[otl])

        trl = TransactionLine.objects.get()
        count_refund = -2
        count_refund2 = -2
        count_refund_new = -2
        rfl = RefundTransactionLine(count=count_refund, price=p, sold_transaction_line=trl)
        rfl2 = RefundTransactionLine(count=count_refund2, price=p, sold_transaction_line=trl)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount * (count_refund + count_refund2),
                          currency=Currency(USED_CURRENCY))
        nega_payment = Payment(amount=loc_money, payment_type=self.pt)
        Transaction.create_transaction(user=self.copro, payments=[nega_payment], transaction_lines=[rfl, rfl2])
        rfl3 = RefundTransactionLine(count=count_refund_new, price=p, sold_transaction_line=trl)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount * count_refund_new,
                          currency=Currency(USED_CURRENCY))
        last_payment = Payment(amount=loc_money, payment_type=self.pt)
        with self.assertRaises(RefundError):
            Transaction.create_transaction(user=self.copro, payments=[last_payment], transaction_lines=[rfl3])


class TestSalesFeaturesWithMixin(TestCase, TestData):

    def setUp(self):
        self.setup_base_data()

    def test_other_cost(self):
        oth_count = 8
        self.create_custorders(othercost_1=oth_count)
        self.create_suporders()
        self.create_packingdocuments()
        self.register_3.open(Decimal(0))
        octl_1 = OtherCostTransactionLine(price=self.price_system_currency_1, count=oth_count,
                                          other_cost_type=self.othercosttype_1, order=1)
        money_3 = Money(amount=self.price_system_currency_1.amount * oth_count, currency=self.price_system_currency_1.currency)
        pymnt_3 = Payment(amount=money_3, payment_type=self.paymenttype_maestro)
        Transaction.create_transaction(user=self.user_2, payments=[pymnt_3], transaction_lines=[octl_1],
                                       customer=self.customer_person_2)
        octl_1 = OtherCostTransactionLine(price=self.price_system_currency_1, count=1,
                                          other_cost_type=self.othercosttype_1, order=1)
        money_3 = Money(amount=self.price_system_currency_1.amount * 1, currency=self.price_system_currency_1.currency)
        pymnt_3 = Payment(amount=money_3, payment_type=self.paymenttype_maestro)
        with self.assertRaises(NotEnoughOrderLinesError):
            Transaction.create_transaction(user=self.user_2, payments=[pymnt_3], transaction_lines=[octl_1],
                                           customer=self.customer_person_2)

    def test_refund_stock_amount(self):
        self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments(article_1=3)
        self.create_transactions_article_type_for_order(article_1=2)
        stl = SalesTransactionLine.objects.get(article=self.articletype_1)
        rfl_1 = RefundTransactionLine(price=self.price_system_currency_1, count=-1, sold_transaction_line=stl)
        money_1 = Money(amount=self.price_system_currency_1.amount * -1, currency=self.price_system_currency_1.currency)
        pymnt_1 = Payment(amount=money_1, payment_type=self.paymenttype_maestro)
        st_level = Stock.objects.get(article=self.articletype_1)
        self.assertEqual(st_level.count, 1)
        Transaction.create_transaction(user=self.user_2, payments=[pymnt_1], transaction_lines=[rfl_1],
                                       customer=self.customer_person_2)
        st_level = Stock.objects.get(article=self.articletype_1, labeltype__isnull=True)
        self.assertEqual(st_level.count, 1)

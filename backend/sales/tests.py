from decimal import Decimal

from django.test import TestCase
from swipe.settings import USED_CURRENCY

from article.models import ArticleType, OtherCostType
from article.tests import INeedSettings
from crm.models import User, Person
from logistics.models import SupplierOrder, StockWish
from money.models import Currency, Cost, Money, VAT, Price, AccountingGroup, CurrencyData
from order.models import Order, OrderLine
from register.models import PaymentType, Register, RegisterMaster, RegisterCount
from sales import models
from sales.models import SalesTransactionLine, Payment, Transaction, NotEnoughStockError, \
    OtherCostTransactionLine, OtherTransactionLine, TransactionLine, PaymentMisMatchError, NotEnoughOrderLinesError, \
    PaymentTypeError, RefundTransactionLine, RefundError, InvalidDataException, StockCollections, PriceOverride
from stock.models import Stock, StockChangeSet
from stock.stocklabel import OrderLabel
from supplication.models import PackingDocument
from supplier.models import Supplier, ArticleTypeSupplier
from tools.testing import TestData


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
class TestTransactionCreationFunction(TestCase, TestData):
    def setUp(self):
        self.setup_base_data()
        self.vat_group = self.vat_group_high
        self.price = Price(amount=Decimal("1.00"), use_system_currency=True)
        self.currency = Currency(iso=USED_CURRENCY)

        self.acc_group = self.accounting_group_components

        self.article_type = self.articletype_1
        self.at2 = self.articletype_2
        self.at3 = ArticleType(accounting_group=self.acc_group, name="Foo3")
        self.at3.save()

        cost = Cost(amount=Decimal(1), use_system_currency=True)

        self.supplier = self.supplier_1

        ats = self.articletypesupplier_article_1
        ats2 = self.articletypesupplier_article_2
        self.money = Money(amount=Decimal(3.32), currency=self.currency)

        self.customer = self.customer_person_1

        self.copro = self.user_1

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

        self.other_cost = OtherCostType(name="Oth1", accounting_group=self.acc_group,
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
        order = Order.create_order_from_wishables_combinations(self.copro, self.customer,
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
                                   count=count, article=self.article_type, order=order.id)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount * count, currency=Currency(USED_CURRENCY))
        local_payment = Payment(amount=loc_money, payment_type=self.pt)
        Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[stl])
        tls = TransactionLine.objects.all()
        self.assertEquals(len(tls), 1)
        obj = tls[0]
        self.assertEquals(obj.num, self.article_type.id)
        self.assertEquals(obj.count, 2)
        self.assertFalse(obj.isRefunded)
        self.assertEquals(obj.order, order.id)
        self.assertEquals(obj.text, str(self.article_type))
        st = Stock.objects.get(labeltype="Order", labelkey=order.id, article=self.article_type)
        self.assertEquals(st.count, AMOUNT_1 - count)
        ols_1 = OrderLine.objects.filter(wishable__sellabletype=self.article_type, state='S')
        ols_2 = OrderLine.objects.filter(wishable__sellabletype=self.article_type, state='A')
        ols = OrderLine.objects.filter(wishable__sellabletype=self.article_type)
        self.assertEquals(len(ols_1), count)
        self.assertEquals(len(ols_2), AMOUNT_1 - count)

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
        self.assertEquals(st.count, AMOUNT_STOCK_1 - count)

    def test_sales_all_stock_levels(self):
        AMOUNT_STOCK_1 = 5
        AMOUNT_ORDER = 4
        order= Order.create_order_from_wishables_combinations(user=self.copro, customer=self.customer,
                                                       wishable_type_number_price_combinations=[[self.article_type,
                                                                                                 AMOUNT_ORDER,
                                                                                                 self.price]])
        StockWish.create_stock_wish(user_modified=self.copro, articles_ordered=[(self.article_type, AMOUNT_STOCK_1)])
        SupplierOrder.create_supplier_order(supplier=self.supplier,
                                            articles_ordered=[[self.article_type, AMOUNT_STOCK_1 + AMOUNT_ORDER,
                                                               self.cost]],
                                            user_modified=self.copro)
        PackingDocument.create_packing_document(user=self.copro, supplier=self.supplier,
                                                article_type_cost_combinations=[[self.article_type,
                                                                                 AMOUNT_STOCK_1 + AMOUNT_ORDER]],
                                                packing_document_name="Foo")
        count_stock = 3
        count_order = 2
        stl = SalesTransactionLine(
            price=Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True, vat=1.23),
            count=count_stock, article=self.article_type, order=None)
        stl2 = SalesTransactionLine(
            price=Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True, vat=1.23),
            count=count_order, article=self.article_type, order=order.id)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount * (count_stock + count_order),
                          currency=Currency(USED_CURRENCY))
        local_payment = Payment(amount=loc_money, payment_type=self.pt)
        Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[stl, stl2])
        st = Stock.objects.get(labeltype__isnull=True, article=self.article_type)
        self.assertEquals(st.count, AMOUNT_STOCK_1 - count_stock)
        st2 = Stock.objects.get(labeltype="Order", labelkey=order.id, article=self.article_type)
        self.assertEquals(st2.count, AMOUNT_ORDER - count_order)

    def test_sales_transaction_not_enough_stock(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        order = Order.create_order_from_wishables_combinations(self.copro, self.customer,
                                                       [[self.article_type, AMOUNT_1, self.price],
                                                        [self.at2, AMOUNT_2, self.price]])
        SupplierOrder.create_supplier_order(self.copro, self.supplier,
                                            articles_ordered=[[self.article_type, AMOUNT_1, self.cost],
                                                              [self.at2, AMOUNT_2, self.cost]])
        PackingDocument.create_packing_document(user=self.copro, supplier=self.supplier,
                                                article_type_cost_combinations=[[self.article_type, AMOUNT_1],
                                                                                [self.at2, AMOUNT_2]],
                                                packing_document_name="Foo")
        count = AMOUNT_1 + 1
        stl = SalesTransactionLine(price=Price(amount=self.simple_payment_eur.amount.amount, use_system_currency=True,
                                               vat=1.23),
                                   count=count, article=self.article_type, order=order.id)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount * count, currency=Currency(USED_CURRENCY))
        local_payment = Payment(amount=loc_money, payment_type=self.pt)
        with self.assertRaises(NotEnoughStockError):
            Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[stl])

    def test_sales_transaction_just_enough_stock(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        order = Order.create_order_from_wishables_combinations(self.copro, self.customer,
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
                                   count=count, article=self.article_type, order=order.id)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount * count, currency=Currency(USED_CURRENCY))
        local_payment = Payment(amount=loc_money, payment_type=self.pt)

        Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[stl])

    def test_sales_transaction_too_much_payment(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        order = Order.create_order_from_wishables_combinations(self.copro, self.customer,
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
                                   count=count, article=self.article_type, order=order.id)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount * count + Decimal(0.001),
                          currency=Currency(USED_CURRENCY))
        local_payment = Payment(amount=loc_money, payment_type=self.pt)

        with self.assertRaises(PaymentMisMatchError):
            Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[stl])

    def test_sales_transaction_too_little_payment(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        order = Order.create_order_from_wishables_combinations(self.copro, self.customer,
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
                                   count=count, article=self.article_type, order=order.id)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount * count - Decimal(0.001),
                          currency=Currency(USED_CURRENCY))
        local_payment = Payment(amount=loc_money, payment_type=self.pt)
        with self.assertRaises(PaymentMisMatchError):
            Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[stl])

    def test_sales_transaction_other_cost(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        AMOUNT_3 = 5
        order = Order.create_order_from_wishables_combinations(self.copro, self.customer,
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
        count = AMOUNT_3 - 1
        octt = OtherCostTransactionLine(price=Price(amount=self.simple_payment_eur.amount.amount,
                                                    use_system_currency=True, vat=1.23),
                                        count=count, other_cost_type=self.other_cost, order=order.id)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount * count, currency=Currency(USED_CURRENCY))
        local_payment = Payment(amount=loc_money, payment_type=self.pt)
        Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[octt])
        tls = TransactionLine.objects.all()
        self.assertEquals(len(tls), 1)
        octls = OtherCostTransactionLine.objects.all()
        self.assertEquals(len(octls), 1)
        octl = octls[0]
        self.assertFalse(octl.isRefunded)
        self.assertEquals(octl.count, count)
        self.assertEquals(octl.order, order.id)
        self.assertEquals(octl.text, octl.other_cost_type.name)
        sold_counter = 0
        ols = OrderLine.objects.filter(wishable__sellabletype=self.other_cost, order_id=order.id)
        for ol in ols:
            if ol.state == 'S':
                sold_counter += 1
        self.assertEquals(sold_counter, count)

    def test_sales_transaction_other_cost_just_enough_orderlines(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        AMOUNT_3 = 5
        order = Order.create_order_from_wishables_combinations(self.copro, self.customer,
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
                                        count=count, other_cost_type=self.other_cost, order=order.id)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount * count, currency=Currency(USED_CURRENCY))
        local_payment = Payment(amount=loc_money, payment_type=self.pt)
        Transaction.create_transaction(user=self.copro, payments=[local_payment], transaction_lines=[octt])
        tls = TransactionLine.objects.all()
        self.assertEquals(len(tls), 1)
        octls = OtherCostTransactionLine.objects.all()
        self.assertEquals(len(octls), 1)
        octl = octls[0]
        self.assertFalse(octl.isRefunded)
        self.assertEquals(octl.count, count)
        self.assertEquals(octl.order, order.id)
        self.assertEquals(octl.text, octl.other_cost_type.name)
        sold_counter = 0
        ols = OrderLine.objects.filter(wishable__sellabletype=self.other_cost, order_id=order.id)
        for ol in ols:
            if ol.state == 'S':
                sold_counter += 1
        self.assertEquals(sold_counter, count)

    def test_sales_transaction_other_cost_not_enough_orderlines(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        AMOUNT_3 = 5
        order = Order.create_order_from_wishables_combinations(self.copro, self.customer,
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
        count = AMOUNT_3 + 1
        octt = OtherCostTransactionLine(price=Price(amount=self.simple_payment_eur.amount.amount,
                                                    use_system_currency=True, vat=1.23),
                                        count=count, other_cost_type=self.other_cost, order=order.id)
        loc_money = Money(amount=self.simple_payment_eur.amount.amount * count, currency=Currency(USED_CURRENCY))
        local_payment = Payment(amount=loc_money, payment_type=self.pt)
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
        loc_money = Money(amount=self.simple_payment_eur.amount.amount * count, currency=Currency(USED_CURRENCY))
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
        loc_money = Money(amount=self.simple_payment_eur.amount.amount * count, currency=Currency("USD"))
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
        loc_money = Money(amount=self.simple_payment_eur.amount.amount * count - Decimal(1),
                          currency=Currency(USED_CURRENCY))
        local_payment = Payment(amount=loc_money, payment_type=self.pt)
        local_payment2 = Payment(amount=Money(amount=Decimal(1), currency=Currency(USED_CURRENCY)),
                                 payment_type=self.pt2)
        Transaction.create_transaction(user=self.copro, payments=[local_payment, local_payment2],
                                       transaction_lines=[otl])

    def test_sales_transaction_mixed_transaction_lines(self):
        AMOUNT_1 = 6
        AMOUNT_2 = 10
        AMOUNT_3 = 5
        order = Order.create_order_from_wishables_combinations(self.copro, self.customer,
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
        stl_1 = SalesTransactionLine(count=count_1, price=p, article=self.article_type, order=order.id)
        stl_2 = SalesTransactionLine(count=count_2, price=p, article=self.at2, order=order.id)
        octl = OtherCostTransactionLine(count=count_3, price=p, other_cost_type=self.other_cost)
        otl = OtherTransactionLine(count=count_4, price=p, text="Rand", accounting_group=self.acc_group)
        loc_money = Money(amount=Decimal(1) * total_count - Decimal(1), currency=Currency(USED_CURRENCY))
        local_payment = Payment(amount=loc_money, payment_type=self.pt)
        local_payment2 = Payment(amount=Money(amount=Decimal(1), currency=Currency(USED_CURRENCY)),
                                 payment_type=self.pt2)
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
        loc_money = Money(amount=self.simple_payment_eur.amount.amount * count_refund_total,
                          currency=Currency(USED_CURRENCY))
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
        order = self.create_custorders(othercost_1=oth_count)
        self.create_suporders()
        self.create_packingdocuments()
        self.register_3.open(Decimal(0))
        octl_1 = OtherCostTransactionLine(price=self.price_system_currency_1, count=oth_count,
                                          other_cost_type=self.othercosttype_1, order=order.id)
        money_3 = Money(amount=self.price_system_currency_1.amount * oth_count,
                        currency=self.price_system_currency_1.currency)
        pymnt_3 = Payment(amount=money_3, payment_type=self.paymenttype_maestro)
        Transaction.create_transaction(user=self.user_2, payments=[pymnt_3], transaction_lines=[octl_1],
                                       customer=self.customer_person_2)
        octl_1 = OtherCostTransactionLine(price=self.price_system_currency_1, count=1,
                                          other_cost_type=self.othercosttype_1, order=order.id)
        money_3 = Money(amount=self.price_system_currency_1.amount * 1, currency=self.price_system_currency_1.currency)
        pymnt_3 = Payment(amount=money_3, payment_type=self.paymenttype_maestro)
        with self.assertRaises(NotEnoughOrderLinesError):
            Transaction.create_transaction(user=self.user_2, payments=[pymnt_3], transaction_lines=[octl_1],
                                           customer=self.customer_person_2)

    def test_refund_stock_amount(self):
        order = self.create_custorders()
        self.create_suporders()
        self.create_packingdocuments(article_1=3)
        self.create_transactions_article_type_for_order(article_1=2, order=order.id)
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

    def test_no_matching_currency(self):
        rupee = CurrencyData(iso="INR", name="Indian Rupee", digits=2, symbol="₹")
        rupee.save()
        new_register = Register(name="Rupee Maestro", currency=rupee, payment_type=self.paymenttype_maestro)
        new_register.save()
        new_register.open(Decimal(0))
        self.create_custorders()
        oth_count = 2
        octl_1 = OtherCostTransactionLine(price=self.price_system_currency_1, count=oth_count,
                                          other_cost_type=self.othercosttype_1, order=1)
        money_3 = Money(amount=self.price_system_currency_1.amount * oth_count,
                        currency=self.price_system_currency_1.currency)
        pymnt_3 = Payment(amount=money_3, payment_type=self.paymenttype_maestro)
        with self.assertRaises(PaymentTypeError):
            Transaction.create_transaction(user=self.user_2, payments=[pymnt_3], transaction_lines=[octl_1],
                                       customer=self.customer_person_2)

    def test_mixing_payment_currency(self):
        rupee = CurrencyData(iso="INR", name="Indian Rupee", digits=2, symbol="₹")
        rupee.save()
        new_register = Register(name="Rupee Maestro", currency=rupee, payment_type=self.paymenttype_maestro)
        new_register.save()
        new_register.open(Decimal(0))
        # Fake transaction with indian rupees, this cannot be done without changing the USED_CURRENCY
        # string which is not possible in this test environment
        transaction = Transaction(salesperiod=RegisterMaster.get_open_sales_period(), customer=None,
                                  user_modified=self.user_1)
        super(Transaction, transaction).save()
        price = Price(amount=Decimal(1), currency=Currency("INR"), vat=Decimal("1"))
        money = Money(amount=Decimal(1), currency=Currency("INR"))
        transaction_line = OtherCostTransactionLine(other_cost_type=self.othercosttype_1, transaction=transaction,
                                                    num=self.othercosttype_1.pk, text="Foo", order=None,
                                                    accounting_group=self.accounting_group_components, price=price,
                                                    user_modified=self.user_1, count=1)
        super(TransactionLine, transaction_line).save()
        payment = Payment(transaction=transaction, amount=money, payment_type=self.paymenttype_maestro)
        super(Payment, payment).save()
        self.register_3.open(Decimal(0))
        octl_1 = OtherCostTransactionLine(price=self.price_system_currency_1, count=1,
                                          other_cost_type=self.othercosttype_1, order=None)
        money_3 = Money(amount=self.price_system_currency_1.amount * 1,
                        currency=self.price_system_currency_1.currency)
        pymnt_3 = Payment(amount=money_3, payment_type=self.paymenttype_maestro)
        with self.assertRaises(PaymentTypeError):
            Transaction.create_transaction(user=self.user_2, payments=[pymnt_3], transaction_lines=[octl_1],
                                       customer=self.customer_person_2)

    def test_original_pricing_price_override(self):
        self.create_externalisation()
        self.register_3.open(Decimal(0))
        octl_1 = OtherCostTransactionLine(price=self.price_system_currency_1, count=1,
                                          other_cost_type=self.othercosttype_1, order=None,
                                          original_price=PriceOverride(original_price=self.price_systen_currency_2, user=self.user_1, reason="Banaan"))
        money_3 = Money(amount=self.price_system_currency_1.amount * 1,
                        currency=self.price_system_currency_1.currency)
        pymnt_3 = Payment(amount=money_3, payment_type=self.paymenttype_maestro)
        Transaction.create_transaction(user=self.user_2, payments=[pymnt_3], transaction_lines=[octl_1],
                                       customer=self.customer_person_2)
        octl = OtherCostTransactionLine.objects.get()
        original_price = PriceOverride.objects.get()
        self.assertEqual(octl.original_price, original_price)

    def test_no_price_override_returns_null(self):
        self.create_externalisation()
        self.register_3.open(Decimal(0))
        octl_1 = OtherCostTransactionLine(price=self.price_system_currency_1, count=1,
                                          other_cost_type=self.othercosttype_1, order=None)
        money_3 = Money(amount=self.price_system_currency_1.amount * 1,
                        currency=self.price_system_currency_1.currency)
        pymnt_3 = Payment(amount=money_3, payment_type=self.paymenttype_maestro)
        Transaction.create_transaction(user=self.user_2, payments=[pymnt_3], transaction_lines=[octl_1],
                                       customer=self.customer_person_2)
        octl = OtherCostTransactionLine.objects.get()
        self.assertIsNone(octl.original_price)


class StockTests(TestCase, TestData):

    def setUp(self):
        self.setup_base_data()
        self.articletype_1.fixed_price = self.price_system_currency_1
        self.articletype_1.save()
        self.articletype_2.fixed_price = self.price_systen_currency_2
        self.articletype_2.save()

    def test_get_stock_for_customer(self):
        changeset = [{
            'article': self.articletype_1,
            'book_value': self.cost_system_currency_1,
            'count': 3,
            'is_in': True,
            'label': OrderLabel(1)
        },
            {
                'article': self.articletype_1,
                'book_value': self.cost_system_currency_1,
                'count': 5,
                'is_in': True,
            },
            {
                'article': self.articletype_2,
                'book_value': self.cost_system_currency_2,
                'count': 6,
                'is_in': True,
            },
            {
                'article': self.articletype_2,
                'book_value': self.cost_system_currency_2,
                'count': 7,
                'is_in': True,
                'label': OrderLabel(2)
            }
        ]

        StockChangeSet.construct(description="Bla", entries=changeset, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        result = StockCollections.get_stock_with_prices(self.customer_person_1)
        self.assertEqual(len(result), 2)
        for line in result:
            if line[0].article == self.articletype_1:
                self.assertEqual(line[0].count, 5)
                self.assertEqual(line[1].amount, self.price_system_currency_1.amount)
            else:
                self.assertEqual(line[0].count, 6)
                self.assertEqual(line[1].amount, self.price_systen_currency_2.amount)

    def test_get_order_stock_for_customers(self):
        self.create_custorders()
        self.create_suporders()
        PACK_ART_1 = 3
        PACK_ART_2 = 4
        self.create_packingdocuments(article_1=PACK_ART_1, article_2=PACK_ART_2)
        result = StockCollections.get_stock_for_customer_with_prices(customer=self.customer_person_1)
        correct_price = {self.articletype_1: self.price_system_currency_1,
                         self.articletype_2: self.price_systen_currency_2}
        correct_amount = {self.articletype_1: PACK_ART_1,
                          self.articletype_2: PACK_ART_2}
        for line in result:
            self.assertEqual(line[1], correct_price.get(line[0].article))
            self.assertEqual(line[0].count, correct_amount.get(line[0].article))

    def test_get_mixed_orders_only_get_correct_ones(self):
        self.create_custorders(article_1=5,article_2=7, customer=self.customer_person_1)
        self.create_custorders(article_1=2, article_2=3, customer=self.customer_person_2)
        self.create_suporders(article_1=7, article_2=10)
        self.create_packingdocuments(article_1=7, article_2=10)
        result = StockCollections.get_stock_for_customer_with_prices(customer=self.customer_person_1)
        for line in result:
            self.assertTrue(line[0].count in [5, 7])
        result2 = StockCollections.get_stock_for_customer_with_prices(customer=self.customer_person_2)
        for line in result2:
            self.assertTrue(line[0].count in [2, 3])

    def test_get_only_stock_mixed(self):
        self.create_custorders(article_1=5, article_2=7, customer=self.customer_person_1)
        self.create_stockwish(article_1=1, article_2=0)
        self.create_suporders(article_1=6, article_2=7)
        self.create_packingdocuments(article_1=6, article_2=7)
        result = StockCollections.get_stock_with_prices(customer=self.customer_person_1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0].count, 1)
        self.assertEqual(result[0][0].article, self.articletype_1)





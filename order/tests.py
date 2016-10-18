from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from article.models import ArticleType, OtherCostType
from article.tests import INeedSettings
from assortment.models import AssortmentArticleBranch
from crm.models import Person
from money.models import VAT, Price, Currency, AccountingGroup, Money, Cost
from order import models
from order.models import Order, OrderLine, OrderLineState, OrderCombinationLine
from register.models import ConsistencyChecker
from stock.models import StockChangeSet
from stock.stocklabel import OrderLabel

# Create your tests here.


class OrderTest(INeedSettings, TestCase):

    def setUp(self):
        super().setUp()
        self.vat_group = VAT()
        self.vat_group.name = "Bar"
        self.vat_group.active = True
        self.vat_group.vatrate = 1.12
        self.vat_group.save()
        self.price = Price(amount=Decimal("1.00"), use_system_currency=True)
        self.currency = Currency(iso="USD")

        self.acc_group = AccountingGroup()
        self.acc_group.accounting_number = 2
        self.acc_group.vat_group = self.vat_group
        self.acc_group.save()

        self.article_type = ArticleType(accounting_group=self.acc_group,
                                        name="Foo", branch=self.branch)
        self.article_type.save()

        self.at2 = ArticleType(accounting_group=self.acc_group,
                               name="Bar", branch=self.branch)
        self.at2.save()

        self.money = Money(amount=Decimal(3.32), currency=self.currency)
        self.oc = OtherCostType(name="Baz", branch=self.branch, accounting_group=self.acc_group, fixed_price=self.money)
        self.oc.save()

        self.customer = Person()
        self.customer.save()

        self.copro = User()
        self.copro.save()

        self.order = Order(user_modified=self.copro, customer=self.customer)
        self.order.save()

    def test_save_speed(self):
        big_order = Order(user_modified=self.copro, customer=self.customer)
        big_order.save()
        orderlines = []
        for i in range(0, 100):
            order_line = OrderLine(order=big_order, wishable=self.article_type, expected_sales_price=self.price,user_modified=self.copro)
            orderlines.append(order_line)

        for ol in orderlines:
            ol.save()

    def test_orderline_storing(self):
        # Simple orderline with customer order
        ol = OrderLine(user_modified=self.copro,order=self.order, wishable=self.article_type, expected_sales_price=self.price)
        ol.save()
        orderlinestates = OrderLineState.objects.filter(orderline=ol)

        self.assertEquals(orderlinestates[0].state , 'O')  # States must match
        self.assertEquals(len(orderlinestates), 1)  # Orderlinestate must be automatically added

        ol2 = OrderLine(user_modified=self.copro,order=self.order, wishable=self.article_type, state='L', expected_sales_price=self.price)
        ol2.save()
        orderlinestates = OrderLineState.objects.filter(orderline=ol2)
        self.assertEquals(orderlinestates[0].state, 'L')  # Self applied state
        self.assertEquals(len(orderlinestates), 1)  # Exactly one state

        ol3 = OrderLine(user_modified=self.copro,)
        with self.assertRaises(models.IncorrectDataError):
            ol3.save()

    def test_illegal_state(self):
        # State must be valid
        with self.assertRaises(models.IncorrectOrderLineStateError):
            ol = OrderLine(user_modified=self.copro, order=self.order, wishable=self.article_type, state='G', expected_sales_price=self.price)
            ol.save()

    def test_transitions(self):
        # Assert transitions for a single orderline
        ol = OrderLine(user_modified=self.copro, order=self.order, wishable=self.article_type, expected_sales_price=self.price)
        ol.save()
        orderlinestates = OrderLineState.objects.filter(orderline=ol)
        self.assertEquals(ol.state, 'O')
        self.assertEquals(len(orderlinestates), 1)
        ol.order_at_supplier(user_created=self.copro)
        orderlinestates = OrderLineState.objects.filter(orderline=ol)
        self.assertEquals(ol.state, 'L')
        self.assertEquals(len(orderlinestates), 2)
        ol.arrive_at_store(user_created=self.copro)
        orderlinestates = OrderLineState.objects.filter(orderline=ol)
        self.assertEquals(ol.state, 'A')
        self.assertEquals(len(orderlinestates), 3)
        ol.sell(user_created=self.copro)
        orderlinestates = OrderLineState.objects.filter(orderline=ol,)
        self.assertEquals(ol.state, 'S')
        self.assertEquals(len(orderlinestates), 4)

    def test_othercost(self):
        ol = OrderLine(user_modified=self.copro,order=self.order, wishable=self.oc, expected_sales_price=self.price)
        ol.save()
        self.assertEquals(ol.state, 'A')
        self.assertEquals(len(OrderLineState.objects.all()), 1)

    def test_illegal_transition(self):
        ol = OrderLine(user_modified=self.copro,order=self.order, wishable=self.article_type, expected_sales_price=self.price)
        ol.save()
        orderlinestates = OrderLineState.objects.filter(orderline=ol)
        self.assertEquals(ol.state, 'O')
        self.assertEquals(len(orderlinestates), 1)
        with self.assertRaises(models.IncorrectTransitionError):
            ol.sell(self.copro)

    def test_order_storage(self):
        order = Order(user_modified=self.copro, customer=self.customer)
        orderlines = []
        orderlines.append(OrderLine(user_modified=self.copro,wishable=self.article_type, expected_sales_price=self.price))
        orderlines.append(OrderLine(user_modified=self.copro,wishable=self.article_type, expected_sales_price=self.price))
        orderlines.append(OrderLine(user_modified=self.copro,wishable=self.article_type, expected_sales_price=self.price))
        Order.make_order(order, orderlines,self.copro)
        ols = OrderLine.objects.filter(order=order)
        self.assertEquals(len(ols), 3)
        self.assertEquals(ols[0].state, 'O')
        errors = ConsistencyChecker.non_crashing_full_check()
        self.assertEquals(len(errors), 0)

    def test_add_group_of_wishables(self):
        orderlines = []
        OrderLine.add_orderlines_to_list(orderlines, self.article_type, 50, self.price,self.copro)
        self.assertEquals(len(orderlines), 50)
        OrderLine.add_orderlines_to_list(orderlines, self.at2, 10, self.price,self.copro)
        self.assertEquals(len(orderlines), 60)
        order = Order(customer=self.customer,user_modified=self.copro)
        Order.make_order(order, orderlines, self.copro)

    def test_print_ol(self):
        orderlines = []
        OrderLine.add_orderlines_to_list(orderlines, self.article_type, 5, self.price,self.copro)
        OrderLine.add_orderlines_to_list(orderlines, self.at2, 3, self.price,self.copro)
        order = Order(customer=self.customer)
        Order.make_order(order, orderlines,self.copro)
        # print("\n")
        # order.print_orderline_info()

    def test_alt_currency(self):
        ol = OrderLine(user_modified=self.copro,order=self.order, wishable=self.article_type, expected_sales_price= Price(amount=Decimal(2), currency=self.currency))

        ol.save()
        ol2 = OrderLine.objects.get()
        self.assertEquals(ol2.expected_sales_price_currency, "USD")

    def test_olc(self):
        ol = OrderLine(user_modified=self.copro,order=self.order, wishable=self.article_type, expected_sales_price=self.price)
        ol.temp = Price(amount=Decimal(2), currency=self.currency)
        ol.save()
        order = Order(user_modified=self.copro, customer=self.customer)
        orderlines = []
        OrderLine.add_orderlines_to_list(orderlines, self.article_type, 5, self.price,self.copro)
        Order.make_order(order, orderlines,self.copro)
        ol = OrderLine(user_modified=self.copro,order=self.order, wishable=self.at2, expected_sales_price=Price(amount=Decimal("3.143"), currency=self.currency))
        ol.save()
        OrderCombinationLine.get_ol_combinations()

    def test_olc_noprice(self):
        order = Order(user_modified=self.copro, customer=self.customer)
        orderlines = []
        local_second_price = Price(amount=Decimal(183839), use_system_currency=True)
        OrderLine.add_orderlines_to_list(orderlines, self.article_type, 5, self.price,self.copro)
        OrderLine.add_orderlines_to_list(orderlines, self.article_type, 5, local_second_price,self.copro)
        Order.make_order(order, orderlines,self.copro)
        olcl=OrderCombinationLine.get_ol_combinations(order=order)
        self.assertEquals(len(olcl), 2)
        olcl2=OrderCombinationLine.get_ol_combinations(order=order, include_price_field=False)
        self.assertEquals(len(olcl2), 1)

    def test_create_order_function(self):
        self.order.delete()
        Order.create_order_from_wishables_combinations(self.copro, self.customer, [[self.article_type, 5, self.price]])
        # Asserts that there is only one Order
        a = Order.objects.get()
        b = OrderLine.objects.filter(order=a)
        c = OrderLine.objects.all()
        self.assertEquals(len(b), len(c))
        self.assertEquals(len(b), 5)
        for i in range(0, len(b)):
            self.assertEquals(b[i].pk, c[i].pk)

    def test_create_order_function_more_sets(self):
        self.order.delete()
        Order.create_order_from_wishables_combinations(self.copro, self.customer, [[self.article_type, 5, self.price],
                                                                                   [self.at2, 6, self.price]])
        # Asserts that there is only one Order
        a = Order.objects.get()
        b = OrderLine.objects.filter(order=a)
        c = OrderLine.objects.all()

        self.assertEquals(len(b), len(c))
        self.assertEquals(len(b), 5+6)
        tally_art1, tally_art2 = 0, 0
        for ol in b:
            if ol.wishable.sellabletype.articletype == self.article_type:
                tally_art1 += 1
            elif ol.wishable.sellabletype.articletype == self.at2:
                tally_art2 += 1
        self.assertEquals(tally_art1, 5)
        self.assertEquals(tally_art2, 6)


class TestStockChangeSetFiltering(TestCase, INeedSettings):

    def setUp(self):
        super().setUp()
        self.vat_group = VAT()
        self.vat_group.name = "Bar"
        self.vat_group.active = True
        self.vat_group.vatrate = 1.12
        self.vat_group.save()
        self.price = Price(amount=Decimal("1.00"), use_system_currency=True)
        self.currency = Currency(iso="USD")

        self.acc_group = AccountingGroup()
        self.acc_group.accounting_number = 2
        self.acc_group.vat_group = self.vat_group
        self.acc_group.save()
        self.branch = AssortmentArticleBranch.objects.create(
            name='hoi',
            parent_tag=None)

        self.article_type = ArticleType(accounting_group=self.acc_group,
                                        name="Foo", branch=self.branch)
        self.article_type.save()
        self.eur = Currency(iso="EUR")
        self.cost = Cost(amount=Decimal(3), currency=self.eur)

        self.customer = Person()
        self.customer.save()

        self.copro = User()
        self.copro.save()

        self.order = Order(user_modified=self.copro, customer=self.customer)
        self.order.save()

    def test_signal_not_enough_orderlines(self):
        changeset=[{
            'article': self.article_type,
            'book_value': self.cost,
            'count': 1,
            'is_in': True,
            'label': OrderLabel(1)
        }]
        StockChangeSet.construct(description="Bla", entries=changeset, enum=0)
        changeset = [{
            'article': self.article_type,
            'book_value': self.cost,
            'count': 1,
            'is_in': False,
            'label': OrderLabel(1)
        }]
        with self.assertRaises(models.InconsistencyError):
            StockChangeSet.construct(description="Bla", entries=changeset, enum=0)

    def test_signal_proper(self):
        pk = self.order.pk
        READIED_ORDERLINES = 8
        for i in range(READIED_ORDERLINES):
            line = OrderLine(order=self.order, state='A', wishable=self.article_type,
                             user_modified=self.copro, expected_sales_price=self.price)
            line.save()

        changeset = [{
            'article': self.article_type,
            'book_value': self.cost,
            'count': READIED_ORDERLINES,
            'is_in': True,
            'label': OrderLabel(pk)
        }]

        SOLD_PRODUCTS = 5
        StockChangeSet.construct(description="Bla", entries=changeset, enum=0)
        changeset = [{
            'article': self.article_type,
            'book_value': self.cost,
            'count': SOLD_PRODUCTS,
            'is_in': False,
            'label': OrderLabel(pk)
        }]

        StockChangeSet.construct(description="Bla", entries=changeset, enum=0)
        ols = OrderLine.objects.all()
        correct_state = 0
        for ol in ols:
            if ol.state == 'S':
                correct_state += 1

        self.assertEquals(correct_state, SOLD_PRODUCTS)

    def test_signal_multiple_orders(self):

        pk = self.order.pk
        order_2 = Order(customer=self.customer, user_modified=self.copro)
        order_2.save()
        READIED_ORDERLINES_1 = 4
        READIED_ORDERLINES_2 = 4
        for i in range(READIED_ORDERLINES_1):
            line = OrderLine(order=self.order, state='A', wishable=self.article_type,
                             user_modified=self.copro, expected_sales_price=self.price)
            line.save()

        for i in range(READIED_ORDERLINES_2):
            line = OrderLine(order=order_2, state='A', wishable=self.article_type,
                             user_modified=self.copro, expected_sales_price=self.price)
            line.save()

        changeset = [{
            'article': self.article_type,
            'book_value': self.cost,
            'count': READIED_ORDERLINES_1,
            'is_in': True,
            'label': OrderLabel(pk)
        },
        {
            'article': self.article_type,
            'book_value': self.cost,
            'count': READIED_ORDERLINES_2,
            'is_in': True,
            'label': OrderLabel(order_2.pk)
        } ]

        SOLD_PRODUCTS_1 = 4
        SOLD_PRODUCTS_2 = 2
        StockChangeSet.construct(description="Bla", entries=changeset, enum=0)
        changeset = [{
            'article': self.article_type,
            'book_value': self.cost,
            'count': SOLD_PRODUCTS_1,
            'is_in': False,
            'label': OrderLabel(pk)
        },
            {
                'article': self.article_type,
                'book_value': self.cost,
                'count': SOLD_PRODUCTS_2,
                'is_in': False,
                'label': OrderLabel(order_2.pk)
            },
        ]

        StockChangeSet.construct(description="Bla", entries=changeset, enum=0)
        ols = OrderLine.objects.all()
        correct_state_1 = 0
        correct_state_2 = 0
        for ol in ols:
            if ol.state == 'S':
                if ol.order.pk == 1:
                    correct_state_1 += 1
                else:
                    correct_state_2 += 1

        self.assertEquals(correct_state_1, SOLD_PRODUCTS_1)
        self.assertEquals(correct_state_2, SOLD_PRODUCTS_2)


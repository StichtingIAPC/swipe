from django.test import TestCase
from unittest import skip
from article.models import *
from article.tests import INeedSettings
from money.models import *
from order.models import *
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

        assert orderlinestates[0].state == 'O'  # States must match
        assert len(orderlinestates) == 1  # Orderlinestate must be automatically added

        ol2 = OrderLine(user_modified=self.copro,order=self.order, wishable=self.article_type, state='L', expected_sales_price=self.price)
        ol2.save()
        orderlinestates = OrderLineState.objects.filter(orderline=ol2)
        assert orderlinestates[0].state == 'L'  # Self applied state
        assert len(orderlinestates) == 1  # Exactly one state

        ol3 = OrderLine(user_modified=self.copro,)
        caught = False
        try:
            ol3.save()
        except AssertionError:
            caught = True
        assert caught

    def test_illegal_state(self):
        # State must be valid
        try:
            excepted = False
            ol = OrderLine(user_modified=self.copro,order=self.order, wishable=self.article_type, state='G', expected_sales_price=self.price)
            ol.save()
        except AssertionError:
            excepted = True
        assert excepted

    def test_transitions(self):
        # Assert transitions for a single orderline
        ol = OrderLine(user_modified=self.copro,order=self.order, wishable=self.article_type, expected_sales_price=self.price)
        ol.save()
        orderlinestates = OrderLineState.objects.filter(orderline=ol)
        assert ol.state == 'O'
        assert len(orderlinestates) == 1
        ol.order_at_supplier(user_created=self.copro)
        orderlinestates = OrderLineState.objects.filter(orderline=ol)
        assert ol.state == 'L'
        assert ol.state == 'L'
        assert len(orderlinestates) == 2
        ol.arrive_at_store(user_created=self.copro)
        orderlinestates = OrderLineState.objects.filter(orderline=ol)
        assert ol.state == 'A'
        assert len(orderlinestates) == 3
        ol.sell(user_created=self.copro)
        orderlinestates = OrderLineState.objects.filter(orderline=ol,)
        assert ol.state == 'S'
        assert len(orderlinestates) == 4

    def test_othercost(self):
        ol = OrderLine(user_modified=self.copro,order=self.order, wishable=self.oc, expected_sales_price=self.price)
        ol.save()
        assert ol.state == 'A'
        assert len(OrderLineState.objects.all()) == 1

    def test_illegal_transition(self):
        ol = OrderLine(user_modified=self.copro,order=self.order, wishable=self.article_type, expected_sales_price=self.price)
        ol.save()
        orderlinestates = OrderLineState.objects.filter(orderline=ol)
        assert ol.state == 'O'
        assert len(orderlinestates) == 1
        caught = False
        try:
            ol.sell(self.copro)
        except IncorrectTransitionError:
            caught = True
        assert caught

    def test_order_storage(self):
        order = Order(user_modified=self.copro, customer=self.customer)
        orderlines = []
        orderlines.append(OrderLine(user_modified=self.copro,wishable=self.article_type, expected_sales_price=self.price))
        orderlines.append(OrderLine(user_modified=self.copro,wishable=self.article_type, expected_sales_price=self.price))
        orderlines.append(OrderLine(user_modified=self.copro,wishable=self.article_type, expected_sales_price=self.price))
        Order.make_order(order, orderlines,self.copro)
        ols = OrderLine.objects.filter(order=order)
        assert len(ols) == 3
        assert ols[0].state == 'O'
        errors = ConsistencyChecker.non_crashing_full_check()
        assert len(errors) == 0

    def test_add_group_of_wishables(self):
        orderlines = []
        OrderLine.add_orderlines_to_list(orderlines, self.article_type, 50, self.price,self.copro)
        assert len(orderlines) == 50
        OrderLine.add_orderlines_to_list(orderlines, self.at2, 10, self.price,self.copro)
        assert len(orderlines) == 60
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
        assert ol2.expected_sales_price_currency == "USD"

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
        assert len(olcl) == 2
        olcl2=OrderCombinationLine.get_ol_combinations(order=order, include_price_field=False)
        assert len(olcl2) == 1
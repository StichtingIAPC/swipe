from django.test import TestCase
from unittest import skip
from article.models import *
from money.models import *
from order.models import *
# Create your tests here.



class OrderTest(TestCase):

    def setUp(self):

        self.vat_group = VAT()
        self.vat_group.name="Bar"
        self.vat_group.active=True
        self.vat_group.vatrate=1.12
        self.vat_group.save()

        self.currency = Currency(iso="USD")

        self.acc_group = AccountingGroup()
        self.acc_group.accounting_number = 2
        self.acc_group.vat_group = self.vat_group
        self.acc_group.save()

        self.article_type = ArticleType(accounting_group=self.acc_group,name="Foo")
        self.article_type.save()

        self.at2 = ArticleType(accounting_group=self.acc_group,name="Bar")
        self.at2.save()

        self.customer = Person()
        self.customer.save()

        self.copro = User()
        self.copro.save()

        self.order = Order(copro=self.copro, customer=self.customer)
        self.order.save()

    @skip("Skipped labour intensive test")
    def test_save_speed(self):
        big_order=Order(copro=self.copro, customer=self.customer)
        big_order.save()
        orderlines = []
        for i in range (0, 100):
            orderLine = OrderLine(order=big_order, wishable=self.article_type)
            orderlines.append(orderLine)

        for ol in orderlines:
            ol.save()

    def test_orderline_storing(self):
        # Simple orderline with customer order
        ol = OrderLine(order=self.order, wishable=self.article_type)
        ol.save()
        orderlinestates = OrderLineState.objects.filter(orderline=ol)

        assert orderlinestates[0].state == 'O'  # States must match
        assert len(orderlinestates) == 1  # Orderlinestate must be automatically added

        ol2 = OrderLine(order=self.order, wishable=self.article_type, state='L')
        ol2.save()
        orderlinestates = OrderLineState.objects.filter(orderline=ol2)
        assert orderlinestates[0].state == 'L'  # Self applied state
        assert len(orderlinestates) == 1  # Exactly one state

        ol3 = OrderLine()
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
            ol = OrderLine(order=self.order, wishable=self.article_type, state='G')
            ol.save()
        except AssertionError:
            excepted = True
        assert excepted

    def test_transitions(self):
        # Assert transitions for a single orderline
        ol = OrderLine(order=self.order, wishable=self.article_type)
        ol.save()
        orderlinestates = OrderLineState.objects.filter(orderline=ol)
        assert ol.state == 'O'
        assert len(orderlinestates) == 1
        ol.order_at_supplier()
        orderlinestates = OrderLineState.objects.filter(orderline=ol)
        assert ol.state == 'L'
        assert len(orderlinestates) == 2
        ol.arrive_at_store()
        orderlinestates = OrderLineState.objects.filter(orderline=ol)
        assert ol.state == 'A'
        assert len(orderlinestates) == 3
        ol.sell()
        orderlinestates = OrderLineState.objects.filter(orderline=ol)
        assert ol.state == 'S'
        assert len(orderlinestates) == 4

    def test_illegal_transition(self):
        ol = OrderLine(order=self.order, wishable=self.article_type)
        ol.save()
        orderlinestates = OrderLineState.objects.filter(orderline=ol)
        assert ol.state == 'O'
        assert len(orderlinestates) == 1
        caught = False
        try:
            ol.sell()
        except IncorrectTransitionError:
            caught = True
        assert caught

    def test_order_storage(self):
        order = Order(copro=self.copro, customer=self.customer)
        orderlines = []
        orderlines.append(OrderLine(wishable=self.article_type))
        orderlines.append(OrderLine(wishable=self.article_type))
        orderlines.append(OrderLine(wishable=self.article_type))
        Order.make_order(order, orderlines)
        ols = OrderLine.objects.filter(order=order)
        assert len(ols) == 3
        assert ols[0].state == 'O'

    def test_add_group_of_wishables(self):
        orderlines = []
        OrderLine.add_orderlines_to_list(orderlines, self.article_type, 50, 1.1)
        assert len(orderlines) == 50
        OrderLine.add_orderlines_to_list(orderlines, self.at2, 10, 1.2)
        assert len(orderlines) == 60
        order = Order(copro=self.copro, customer=self.customer)
        Order.make_order(order, orderlines)

    def test_print_ol(self):
        orderlines = []
        OrderLine.add_orderlines_to_list(orderlines, self.article_type, 5, 1.1)
        OrderLine.add_orderlines_to_list(orderlines, self.at2, 3, 1.61)
        order = Order(copro=self.copro, customer=self.customer)
        Order.make_order(order, orderlines)
        print("\n")
        order.print_orderline_info()

    def test_alt_currency(self):
        ol = OrderLine(order=self.order, wishable=self.article_type)
        ol.temp = PriceImitator(amount=2, currency=self.currency)
        ol.save()
        ol2=OrderLine.objects.get()
        assert ol2.expected_sales_price_currency == "USD"

    def test_olc(self):
        ol = OrderLine(order=self.order, wishable=self.article_type)
        ol.temp = PriceImitator(amount=2, currency=self.currency)
        ol.save()
        order = Order(copro=self.copro, customer=self.customer)
        orderlines = []
        OrderLine.add_orderlines_to_list(orderlines, self.article_type, 5, 1.1)
        Order.make_order(order, orderlines)
        ol = OrderLine(order=self.order, wishable=self.at2)
        ol.temp = PriceImitator(amount=3.143, currency=self.currency)
        ol.save()
        OrderCombinationLine.get_ol_combinations()

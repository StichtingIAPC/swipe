from django.db import models
from crm.models import *
from article.models import *
from money.models import *

# Create your models here.


class Order(models.Model):
    # A collection of orders of a customer ordered together
    customer = models.ForeignKey(Customer)

    date = models.DateTimeField(auto_now_add=True)

    copro = models.ForeignKey(User)

    @staticmethod
    def make_order(order, orderlines):
        """
        Creates a new order with the specified orderlines. Order must be unsaved.
        The orderlines need to be valid unsaved orderlines.
        :param order: The order that needs to be saved
        :param orderlines: The orderlines that need to be connected to the order and saved
        """
        assert type(order) == Order
        for ol in orderlines:
            assert type(ol) == OrderLine
        order.save()
        for ol in orderlines:
            ol.order = order
            ol.save()

    def __str__(self):
        return "Customer: {}, Copro: {}, Date: {} ".format(self.customer, self.copro, self.date)

    def print_orderline_info(self):
        if not self.pk > 0:
            print("Unstored")
            return
        orderlines = OrderLine.objects.filter(order=self)
        summary = []
        if len(orderlines) == 0:
            print("Empty")
            return
        wishable = 0
        state = "-"
        price = Price(amount=Decimal(1), currency=Currency(iso='XXX'), vat=1)
        counter = -1
        for i in range(0, len(orderlines)):
            if orderlines[i].wishable.id == wishable and orderlines[i].state == state and \
                    orderlines[i].expected_sales_price == price:
                summary[counter][3] += 1  # Increment object with same state
            else:
                # Create new object in summary list
                counter += 1
                summary.append([orderlines[i].wishable.name, orderlines[i].state,
                                orderlines[i].expected_sales_price, 1])
                price = orderlines[i].expected_sales_price
                wishable = orderlines[i].wishable.id
                state = orderlines[i].state

        print("{:<7}{:14}{:10}{:12}".format("Number", "Article", "ExpPrice", "Status"))
        for j in range(0, len(summary)):
            dec = summary[j][2].amount
            dec = dec.quantize(Decimal('0.01'))
            print("{:<7}{:14}{:10}{:12}".format(summary[j][3], summary[j][0],
                                                summary[j][2].currency.iso + str(dec),
                                                OrderLineState.OL_STATE_MEANING[summary[j][1]]))


class OrderLineState(models.Model):
    # A representation of the state of a orderline
    OL_STATE_CHOICES = ('O', 'L', 'A', 'C', 'S')
    OL_STATE_MEANING = {'O': 'Ordered by Customer', 'L': 'Ordered at Supplier',
                        'A': 'Arrived at Store', 'C': 'Cancelled', 'S': 'Sold'}

    state = models.CharField(max_length=3)

    timestamp = models.DateTimeField(auto_now_add=True)

    orderline = models.ForeignKey('OrderLine')

    def __str__(self):
        return "Orderline_id: {}, State: {}, Timestamp: {}".format(self.orderline.pk, self.state, self.timestamp)

    def save(self):
        assert self.state in OrderLineState.OL_STATE_CHOICES
        super(OrderLineState, self).save()


class PriceImitator:
    def __init__(self, amount=-1, currency=None, vat=None):
        self.amount = amount
        self.currency = currency
        self.vat = vat


class OrderLine(models.Model):
    # An order of a customer for a single product of a certain type
    order = models.ForeignKey(Order)

    wishable = models.ForeignKey(WishableType)

    state = models.CharField(max_length=3)

    expected_sales_price = PriceField()

    temp = PriceImitator()  # Workaround for getting Price to accept input

    @staticmethod
    def create_orderline(order=Order(), wishable=None, state=None, price_imitator=None):
        """
        Function intended to create orderlines. Evades high demands of Price-class. Sets up the basics needed. The rest
        is handled by the save function of orderlines.
        """
        assert wishable
        ol = OrderLine(order=order, wishable=wishable, state=state)
        if type(price_imitator) == PriceImitator:
            ol.temp = price_imitator
        return ol

    def get_type(self):
        return type(self)

    def save(self):
        if self.pk is None:
            if not self.state:
                ol_state = OrderLineState(state='O')
                self.state = 'O'
            else:
                ol_state = OrderLineState(state=self.state)
            assert hasattr(self, 'order')  # Order must exist
            assert hasattr(self, 'wishable')  # Type must exist
            assert self.state in OrderLineState.OL_STATE_CHOICES
            curr = Currency(iso=OrderLine.get_system_currency())
            if self.temp is None:
                self.temp = PriceImitator(amount=-1, currency=curr)
            if self.temp.currency is None:
                self.temp.currency = curr
            self.temp.vat = self.wishable.get_vat()
            pr = Price(amount=Decimal(self.temp.amount), currency=self.temp.currency, vat=self.temp.vat)
            self.expected_sales_price = pr
            super(OrderLine, self).save()
            ol_state.orderline = self
            ol_state.save()
        else:
            super(OrderLine, self).save()

    def transition(self, new_state):
        """
        Transitions an orderline from one state to another. This is the only safe means of transitioning, as data
        integrity can not be guaranteed otherwise. Transitioning is only possible with objects stored in the database.
        """
        if not self.pk or self.state is None:
            raise OrderLineNotSavedError
        elif self.state not in OrderLineState.OL_STATE_CHOICES:
            raise IncorrectOrderLineStateError("State of orderline is not valid. Database might be corrupted")
        elif new_state not in OrderLineState.OL_STATE_CHOICES:
            raise IncorrectTransitionError("New state is not a valid state")
        else:
            if self.state == 'O':
                if new_state in ('C', 'L'):
                    self.state = new_state
                    ols = OrderLineState(state=new_state, orderline=self)
                    ols.save()
                else:
                    raise IncorrectTransitionError("This transition is not legal")
            elif self.state == 'L':
                if new_state in ('A'):
                    self.state = new_state
                    ols = OrderLineState(state=new_state, orderline=self)
                    ols.save()
                else:
                    raise IncorrectTransitionError("This transition is not legal")
            elif self.state == 'A':
                if new_state in ('S'):
                    self.state = new_state
                    ols = OrderLineState(state=new_state, orderline=self)
                    ols.save()
                else:
                    raise IncorrectTransitionError("This transition is not legal")
            else:
                raise IncorrectTransitionError("You cannot transition from this state")

    def order_at_supplier(self):
        self.transition('L')

    def arrive_at_store(self):
        self.transition('A')

    def sell(self):
        self.transition('S')

    def cancel(self):
        self.transition('C')

    def __str__(self):
        if not hasattr(self, 'order'):
            ordr = 'No order'
        else:
            ordr = self.order.pk

        return "Order: {}, Wishable: {}, State: {}, Expected Sales Price: {}, Currency: {}, Vat-rate: {}".\
            format(ordr, self.wishable, self.state, self.expected_sales_price.amount,
                   self.expected_sales_price_currency,
                   self.expected_sales_price_vat)

    @staticmethod
    def add_orderlines_to_list(orderlinelist, wishable_type, number, price):
        """
        Adds a number of orderlines of a certain wishabletype to the orderlinelist
        :param orderlinelist: List to be amended, should only contain orderlines
        :param wishable_type: a wishabletype
        :param number: number of orderlines to add
        :param price: Value as a float
        """
        assert type(number) == int
        assert number >= 1
        for i in range(1, number + 1):
            p = PriceImitator(amount=price, currency=None, vat=None)
            ol = OrderLine.create_orderline(wishable=wishable_type, price_imitator=p)
            orderlinelist.append(ol)

    @staticmethod
    def get_system_currency():
        return 'ABC'


class OrderLineNotSavedError(Exception):
    pass


class IncorrectOrderLineStateError(Exception):
    pass


class IncorrectTransitionError(Exception):
    pass

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
        wishable=0
        state="-"
        counter=-1
        for i in range(0, len(orderlines)):
            if orderlines[i].wishable.id == wishable and orderlines[i].state == state:
                summary[counter][2] += 1 # Increment object with same state
            else:
                #Create new object in summary list
                counter += 1
                summary.append([orderlines[i].wishable.name, orderlines[i].state, 1])
                wishable = orderlines[i].wishable.id
                state = orderlines[i].state

        print("{:<7}{:14}{:12}".format("Number", "Article", "Status"))
        for j in range(0, len(summary)):
            print("{:<7}{:14}{:12}".format(summary[j][2], summary[j][0], OrderLineState.OL_STATE_MEANING[summary[j][1]]))






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


class OrderLine(models.Model):
    # An order of a customer for a single product of a certain type
    order = models.ForeignKey(Order)

    wishable = models.ForeignKey(WishableType)

    state = models.CharField(max_length=3)

    expected_sales_price = MoneyField(no_currency_field=True)

    currency = models.CharField(max_length=3)

    vat_rate = VATLevelField()


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
            if self.expected_sales_price is None:
                self.expected_sales_price = 0.0
            self.vat_rate = self.wishable.get_vat()  # Retrieves VAT-rate from wishable
            self.currency=CurrencyField("ABC")
            #self.currency = CurrencyField(OrderLine.get_system_currency())  # Gets currency from system
            #print(self.currency)
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
        if not hasattr(self,'order'):
            ordr = 'No order'
        else:
            ordr = self.order.pk

        return "Order: {}, Wishable: {}, State: {}".format(ordr, self.wishable, self.state)

    @staticmethod
    def add_orderlines_to_list(orderlinelist, wishable_type, number, price):
        """
        Adds a number of orderlines of a certain wishabletype to the orderlinelist
        :param orderlinelist: List to be amended, should only contain orderlines
        :param wishable_type: a wishabletype
        :param number: number of orderlines to add
        """
        assert type(number) == int
        assert number >= 1
        for i in range(1, number+1):
            ol=OrderLine(wishable=wishable_type, expected_sales_price=price)
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

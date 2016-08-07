from django.db import models
from django.db.models.fields.related import RelatedField
from django.db.models.fields.reverse_related import ForeignObjectRel
from crm.models import *
from article.models import *
from money.models import *
from django.db.models import Count, Prefetch, ForeignObject


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
        ocls = OrderCombinationLine.get_ol_combinations(order=self)
        print("{:<7}{:14}{:10}{:12}".format("Number","Name","Exp.Price","State"))
        for ocl in ocls:
            print(ocl)


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

    temp = PriceImitator()  # Workaround for getting Price to accept input. Used only at creation time.

    @staticmethod
    def create_orderline(order=Order(), wishable=None, state=None, price_imitator=None):
        """
        Function intended to create orderlines. Evades high demands of Price-class. Sets up the basics needed. The rest
        is handled by the save function of orderlines.
        """
        assert wishable is not None
        ol = OrderLine(order=order, wishable=wishable, state=state)
        if type(price_imitator) == PriceImitator:
            ol.temp = price_imitator
        return ol

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
            self.temp.vat = self.wishable.get_vat_rate()
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
            raise IncorrectOrderLineStateError("State of orderline is not valid. Database is corrupted at Orderline",
                                               self.pk, " with state ", self.state)
        elif new_state not in OrderLineState.OL_STATE_CHOICES:
            raise IncorrectTransitionError("New state is not a valid state")
        else:
            nextstates = {
                'O': ('C', 'L'),
                'L': ('A',),
                'A': ('S') }
            if new_state in nextstates[self.state]:
                self.state = new_state
                ols = OrderLineState(state=new_state, orderline=self)
                ols.save()
                self.save()
            else:
                raise IncorrectTransitionError("This transaction is not legal: {state} -> {new_state}".format(state=self.state, new_state=new_state))


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

class OrderCombinationLine():
    """
    Line that combines similar orderlines into one to reduce overal size
    """
    number = 0

    wishable = WishableType

    price = Price

    state = ""

    def __init__(self, wishable, number, price, state):
        self.wishable = wishable
        self.number = number
        self.price = price
        self.state = state

    def __str__(self):
        dec = self.price.amount.quantize(Decimal('0.01'))
        stri = "{:<7}{:14}{:10}{:12}".format(self.number, self.wishable.name , self.price.currency.iso+str(dec),
                                              OrderLineState.OL_STATE_MEANING[self.state])
        return stri
    @staticmethod
    def prefix_field_names(model, prefix):
        fields = model._meta.get_fields()
        ret = []
        for field in fields:
            if not isinstance(field, ForeignObjectRel):
                ret.append(prefix + field.name)
        return ret

    @staticmethod
    def get_ol_combinations(order=None, wishable=None, state=None, qs=OrderLine.objects):
        result = []
        filter={}
        if order:
            filter['order'] = order
        if wishable:
            filter['wishable'] = wishable
        if state:
            filter['state'] = state

        orderlines = qs.filter(**filter).\
            values('state', 'expected_sales_price','expected_sales_price_currency','expected_sales_price_vat', * OrderCombinationLine.\
                   prefix_field_names(WishableType, 'wishable__')).annotate(Count('id'))
        for o in orderlines:
            number=o['id__count']
            state=o['state']
            price=Price(amount=o['expected_sales_price'],currency=Currency(iso=o['expected_sales_price_currency']),
                                        vat=o['expected_sales_price_vat'])
            ocl = OrderCombinationLine(number=number, wishable=WishableType(name=o['wishable__name'], \
                                       pk=o['wishable__id']), price=price,
                                        state=state)
            result.append(ocl)
        return result


class OrderLineNotSavedError(Exception):
    pass


class IncorrectOrderLineStateError(Exception):
    pass


class IncorrectTransitionError(Exception):
    pass

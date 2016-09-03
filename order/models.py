from django.db import models, transaction
from django.db.models.fields.reverse_related import ForeignObjectRel

from blame.models import Blame, ImmutableBlame
from crm.models import *
from article.models import *
from money.models import *
from django.db.models import Count
from swipe.settings import USED_CURRENCY
from tools.management.commands.consistencycheck import consistency_check, CRITICAL


# Create your models here.


class Order(Blame):
    # A collection of orders of a customer ordered together
    # Customer that originates the order
    customer = models.ForeignKey(Customer)

    @staticmethod
    def make_order(order, orderlines,user):
        """
        Creates a new order with the specified orderlines. Order must be unsaved.
        The orderlines need to be valid unsaved orderlines.
        :param order: The order that needs to be saved
        :param orderlines: The orderlines that need to be connected to the order and saved
        """
        assert type(order) == Order
        for ol in orderlines:
            ol.user_modified = user
            assert type(ol) == OrderLine
        order.user_modified=user
        order.save()
        for ol in orderlines:
            ol.order = order
            ol.save()

    def __str__(self):
        return "Customer: {}, Copro: {}, Date: {} ".format(self.customer, self.user_created, self.date_created)

    def print_orderline_info(self):
        ocls = OrderCombinationLine.get_ol_combinations(order=self)
        print("{:<7}{:14}{:10}{:12}".format("Number", "Name", "Exp.Price", "State"))
        for ocl in ocls:
            print(ocl)


class OrderLineState(ImmutableBlame):
    # A representation of the state of a orderline. Can be used as a logging tool for any OrderLine
    OL_STATE_CHOICES = ('O', 'L', 'A', 'C', 'S', 'I')
    OL_STATE_MEANING = {'O': 'Ordered by Customer', 'L': 'Ordered at Supplier',
                        'A': 'Arrived at Store', 'C': 'Cancelled', 'S': 'Sold', 'I' : 'Used for Internal Purposes'}
    # Mirrors the transition of the state of an OrderLine
    state = models.CharField(max_length=3)
    # When did the transition happen?
    timestamp = models.DateTimeField(auto_now_add=True)
    # The OrderLine that is transitioning
    orderline = models.ForeignKey('OrderLine')

    def __str__(self):
        return "Orderline_id: {}, State: {}, Timestamp: {}".format(self.orderline.pk, self.state, self.timestamp)

    def save(self):
        assert self.state in OrderLineState.OL_STATE_CHOICES
        super(OrderLineState, self).save()


class OrderLine(Blame):
    # An order of a customer for a single product of a certain type
    # Collection including this OrderLine
    order = models.ForeignKey(Order)
    # Anything the customer desires and we can supply
    wishable = models.ForeignKey(WishableType)
    # Indicates where in the process this OrderLine is. Every state allows for different actions
    state = models.CharField(max_length=3)
    # The price the customer sees at the moment the Order(Line) is created
    expected_sales_price = PriceField()
    # Final sales price. Set when products arrive at the store
    final_sales_price = PriceField(null=True, default=None)


    @staticmethod
    def create_orderline(order=Order(), wishable=None, state=None, expected_sales_price=None, user=None):
        """
        Function intended to create orderlines. Evades high demands of Price-class. Sets up the basics needed. The rest
        is handled by the save function of orderlines.
        """
        assert wishable is not None
        ol = OrderLine(order=order, wishable=wishable, state=state, expected_sales_price=expected_sales_price, user_modified=user)

        return ol

    def save(self):
        assert hasattr(self, 'order')  # Order must exist
        assert hasattr(self, 'wishable')  # Type must exist
        assert hasattr(self.wishable, 'sellabletype') # Temporary measure until complexities get worked out
        assert hasattr(self, 'expected_sales_price')
        assert isinstance(self.expected_sales_price, Price)  # Temporary measure until complexities get worked out

        if self.pk is None:

            if not self.state:
                if type(self.wishable) == OtherCostType:
                    ol_state = OrderLineState(state='A', user_created=self.user_modified)
                    self.state = 'A'
                else:
                    ol_state = OrderLineState(state='O', user_created=self.user_modified)
                    self.state = 'O'
            else:
                ol_state = OrderLineState(state=self.state, user_created=self.user_modified)

            assert self.state in OrderLineState.OL_STATE_CHOICES
            curr = Currency(iso=USED_CURRENCY)

            self.expected_sales_price =  Price(amount=self.expected_sales_price._amount, currency=self.expected_sales_price._currency, vat=self.wishable.get_vat_rate())

            super(OrderLine, self).save()
            ol_state.orderline = self
            ol_state.save()
        else:
            assert self.state in OrderLineState.OL_STATE_CHOICES
            super(OrderLine, self).save()

    @transaction.atomic
    def transition(self, new_state,user_created):
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
                'L': ('A', 'O', 'C'),
                'A': ('S', 'I')}
            if new_state in nextstates[self.state]:
                self.state = new_state
                ols = OrderLineState(state=new_state, orderline=self,user_created=user_created)
                ols.save()
                self.save()
            else:
                raise IncorrectTransitionError("This transaction is not legal: {state} -> {new_state}".format(state=self.state, new_state=new_state))

    def order_at_supplier(self,user_created):
        self.transition('L',user_created)

    def arrive_at_store(self,user_created):
        self.transition('A',user_created)

    def sell(self,user_created):
        self.transition('S',user_created)

    def cancel(self,user_created):
        self.transition('C',user_created)

    def return_back_to_ordered_by_customer(self, user_created):
        self.transition('O', user_created)

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
    def add_orderlines_to_list(orderlinelist, wishable_type, number, price, user):
        """
        Adds a number of orderlines of a certain wishabletype to the orderlinelist
        :param orderlinelist: List to be amended, should only contain orderlines
        :param wishable_type: a wishabletype
        :param number: number of orderlines to add
        :param price: Value as a Price
        """
        assert type(number) == int
        assert number >= 1
        for i in range(1, number + 1):

            ol = OrderLine.create_orderline(wishable=wishable_type, expected_sales_price=price, user=user)
            orderlinelist.append(ol)


class OrderCombinationLine:
    """
    Line that combines similar orderlines into one to reduce overal size. This can be used to display data in an orderly fashion
    but is also very usefull as a way to retrieve data about large collections of OrderLines. Use this in stead of combining
    database lines directly!
    """
    # The number of a certain wishable in this OrderCombinationLine
    number = 0
    # Any product that can be wished by a customer
    wishable = WishableType
    # The price decided at the moment the customer ordered products
    price = Price
    # State in which a number of wishables are
    state = ""

    def __init__(self, wishable, number, price, state):
        self.wishable = wishable
        self.number = number
        self.price = price
        self.state = state

    def __str__(self):
        dec = self.price.amount.quantize(Decimal('0.01'))
        stri = "{:<7}{:14}{:10}{:12}".format(self.number, self.wishable.name, self.price.currency.iso + str(dec),
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
    def get_ol_combinations(order=None, wishable=None, state=None, qs=OrderLine.objects, include_price_field=True):
        result = []
        filtr = {}
        if order:
            filtr['order'] = order
        if wishable:
            filtr['wishable'] = wishable
        if state:
            filtr['state'] = state

        price_fields = []
        if include_price_field:
            price_fields = ['expected_sales_price','expected_sales_price_currency','expected_sales_price_vat']

        flds = price_fields + OrderCombinationLine.prefix_field_names(WishableType, 'wishable__')

        orderlines = qs.filter(**filtr).\
            values('state', *flds).annotate(Count('id'))
        for o in orderlines:
            number = o['id__count']
            state = o['state']
            if not include_price_field:
                amount = Decimal(-1)
                currency = Currency(iso=USED_CURRENCY)
                vat = 0
            else:
                amount = o['expected_sales_price']
                currency = o['expected_sales_price_currency']
                vat = o['expected_sales_price_vat']
            price = Price(amount=amount, vat=vat, currency=currency)
            ocl = OrderCombinationLine(number=number, wishable=WishableType(name=o['wishable__name'],
                                       pk=o['wishable__id']), price=price,
                                       state=state)
            result.append(ocl)
        return result


class ConsistencyChecker:
    """
    Checks for states in the system that are unlikely to be good are are actively dangerous. Take warning seriously,
    especially those with a higher severity.
    """

    @staticmethod
    @consistency_check
    def non_crashing_full_check():
        errors = []
        ols = OrderLine.objects.all().exclude(state__in=OrderLineState.OL_STATE_CHOICES)
        if len(ols) > 0:
            errors.append({
                "text": "There are OrderLines in an impossible state",
                "location": "OrderLine",
                "line": -1,
                "severity": CRITICAL
            })
        return errors


class OrderLineNotSavedError(Exception):
    pass


class IncorrectOrderLineStateError(Exception):
    pass


class IncorrectTransitionError(Exception):
    pass
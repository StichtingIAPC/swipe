from django.db import models
from crm.models import *
from article.models import *

# Create your models here.


class Order(models.Model):
    # A collection of orders of a customer ordered together
    customer = models.ForeignKey(Customer)

    date = models.DateTimeField(auto_now_add=True)

    copro = models.ForeignKey(User)


class OrderLineState(models.Model):
    # A representation of the state of a orderline
    OL_STATE_CHOICES = ('O', 'L', 'A', 'C', 'S')
    OL_STATE_MEANING = (('O', 'Ordered by Customer'), ('L', 'Ordered at Supplier'), ('A', 'Arrived at Store'), ('C', 'Cancelled'), ('S', 'Sold'))

    state = models.CharField(max_length=3, choices=OL_STATE_CHOICES)

    timestamp = models.DateTimeField(auto_now_add=True)

    orderline = models.ForeignKey('OrderLine')

    def __str__(self):
        return "Orderline_id: {}, State: {}, Timestamp: {}".format(self.orderline.pk, self.state, self.timestamp)


class OrderLine(models.Model):
    # An order of a customer for a single product of a certain type
    order = models.ForeignKey(Order)

    wishable = models.ForeignKey(WishableType)

    state = models.CharField(max_length=3, choices=OrderLineState.OL_STATE_CHOICES)

    def get_type(self):
        return type(self)

    def save(self):
        if self.pk is None:
            if not self.state:
                ol_state = OrderLineState(state='O')
                self.state = 'O'
            else:
                ol_state = OrderLineState(state=self.state)
            assert self.order  # Order must exist
            assert self.wishable  # Type must exist
            assert self.state in OrderLineState.OL_STATE_CHOICES
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
                if new_state == 'C' or new_state == 'L':
                    self.state = new_state
                    ols = OrderLineState(state=new_state, orderline=self)
                    ols.save()
                else:
                    raise IncorrectTransitionError("This transition is not legal")
            elif self.state == 'L':
                if new_state == 'A':
                    self.state = new_state
                    ols = OrderLineState(state=new_state, orderline=self)
                    ols.save()
                else:
                    raise IncorrectTransitionError("This transition is not legal")
            elif self.state == 'A':
                if new_state == 'S':
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


class OrderLineNotSavedError(Exception):
    pass


class IncorrectOrderLineStateError(Exception):
    pass


class IncorrectTransitionError(Exception):
    pass

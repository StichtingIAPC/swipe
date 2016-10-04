from django.db import models, transaction
from crm.models import Customer
from blame.models import Blame, ImmutableBlame


class RMA(Blame):

    # The customer. Null for ourselves as customer
    customer = models.ForeignKey(Customer, null=True)

    # Here, we need a reference to a refundline in order to handle RMAs fully internally. Null inficates no refund or
    # no refund yet given
    # refund_line = models.ForeignKey(RefundLine, null=True)

    def is_active(self):
        return self.is_internally_active() and self.is_customer_active()

    def is_internally_active(self):
        ira = InternalRMA.objects.get(general_rma=self)
        return ira.is_active()

    def is_customer_active(self):
        cra = CustomerRMA.objects.get(general_rma=self)
        return cra.is_active()


class InternalRMA(Blame):

    general_rma = models.ForeignKey(RMA)

    state = models.CharField(max_length=3)
    # An optional serial number to uniquely identify the product
    serial_number = models.CharField(max_length=60, null=True)
    # The RMA-number. Null for nothing(yet)
    rma_number = models.CharField(max_length=60, null=True)

    def save(self, **kwargs):
        if self.pk is None:
            if not self.state:
                self.state = InternalRMAState.STARTING_STATE
        if self.state not in InternalRMAState.RMA_STATES:
            raise StateError("State {} is not in list of allowed states".format(self.state))
        super(InternalRMA, self).save(**kwargs)

    def is_active(self):
        return self.state in InternalRMAState.OPEN_STATES

    @transaction.atomic
    def transition(self, new_state):
        if new_state not in InternalRMAState.RMA_STATES:
            raise StateError("New state \"{}\" not in list of states".format(new_state))
        self.state = new_state
        state_log = InternalRMAState(state=new_state, internal_rma=self)
        state_log.save()
        self.save()

    def indicate_not_broken(self):
        self.transition('N')

    def ask_for_number(self):
        self.transition('W')

    def recieve_number(self, number):
        self.rma_number=number
        self.transition('R')

    def send(self):
        self.transition('S')


class CustomerRMA(Blame):

    general_rma = models.ForeignKey(RMA)

    state = models.CharField(max_length=3)
    # Original customer that caused the refund. Null for anonymous or self
    original_customer = models.ForeignKey(Customer, null=True)

    @transaction.atomic()
    def save(self, **kwargs):
        if self.pk is None:
            if not self.state:
                self.state = CustomerRMAState.STARTING_STATE
        if self.state not in CustomerRMAState.RMA_STATES:
            raise StateError("State {} is not in list of allowed states".format(self.state))
        if self.pk is None:
            state_log = CustomerRMAState(state=self.state, customer_rma=self)
            state_log.save()
        super(CustomerRMA, self).save(**kwargs)

    def is_active(self):
        return self.state in CustomerRMAState.OPEN_STATES

    @transaction.atomic
    def transition(self, new_state):
        if new_state not in CustomerRMAState.RMA_STATES:
            raise StateError("New state \"{}\" not in list of states".format(new_state))
        self.state = new_state
        state_log = CustomerRMAState(state=new_state, customer_rma=self)
        state_log.save()
        self.save()


class InternalRMAState(ImmutableBlame):

    RMA_STATES = ('U', 'N', 'W', 'R', 'S', 'P', 'F', 'A', 'I')
    STARTING_STATE = 'U'
    OPEN_STATES = ('U', 'W', 'R', 'S')
    CLOSED_STATES = ('N', 'P', 'F', 'A')
    RMA_STATE_EXPLANATIONS = {'U': 'Untested', 'N': 'Not broken', 'W': 'Waiting for Number', 'R': 'Received Number',
                              'S': 'Sent', 'P': 'Replaced', 'F': 'Refunded by External',
                              'A': 'Abused by Customer', 'I': 'Written Off'}

    state = models.CharField(max_length=3)
    internal_rma = models.ForeignKey(InternalRMA)


class CustomerRMAState(ImmutableBlame):
    RMA_STATES = ('O', 'L', 'E', 'D')
    STARTING_STATE = 'E'
    OPEN_STATES = ('E')
    CLOSED_STATES = ('O', 'L', 'D')
    RMA_STATE_EXPLANATIONS = {'E': 'Unresolved', 'D': 'Refunded', 'L': 'Replacement product', 'O': 'Returned old product'}

    state = models.CharField(max_length=3)
    customer_rma = models.ForeignKey(CustomerRMA)


class StateError(Exception):
    pass


class MatchingException(Exception):
    pass


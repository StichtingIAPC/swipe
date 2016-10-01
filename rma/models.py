from django.db import models
from crm.models import Customer
from blame.models import Blame, ImmutableBlame


class RMA(Blame):

    # The customer. Null for ourselves as customer
    customer = models.ForeignKey(Customer, null=True)
    # The state in which the RMA is

    # The RMA-number. Null for no
    rma_number = models.CharField(max_length=60, null=True)

    serial_number = models.CharField(max_length=60, null=True)
    # Here, we need a reference to a refundline in order to handle RMAs fully internally


class InternalRMA(Blame):

    general_rma = models.ForeignKey(RMA)

    state = models.CharField(max_length=3)


class CustomerRMA(Blame):

    general_rma = models.ForeignKey(RMA)

    state = models.CharField(max_length=3)


class InternalRMAState(ImmutableBlame):

    RMA_STATES = ('U', 'N', 'W', 'R', 'S', 'P', 'F', 'A')
    OPEN_STATES = ('U', 'W', 'R', 'S')
    CLOSED_STATES = ('N', 'P', 'F', 'A')
    RMA_STATE_EXPLANATIONS = {'U': 'Untested', 'N': 'Not broken', 'W': 'Waiting for Number', 'R': 'Received Number',
                              'S': 'Sent', 'P': 'Replaced', 'F': 'Refunded by External', 'A': 'Abused by Customer'}


class CustomerRMAState(ImmutableBlame):
    RMA_STATES = ('O', 'L', 'E', 'D')
    OPEN_STATES = ('E')
    CLOSED_STATES = ('O', 'L', 'D')
    RMA_STATE_EXPLANATIONS = {'E': 'Unresolved', 'D': 'Refunded', 'L': 'Replacement product', 'O': 'Returned old product'}


from django.db import models
from crm.models import Customer
from blame.models import Blame, ImmutableBlame


class RMA(Blame):

    # The customer. Null for ourselves as customer
    customer = models.ForeignKey(Customer, null=True)
    # The state in which the RMA is
    state = models.CharField(max_length=3)
    # The RMA-number. Null for no
    rma_number = models.CharField(max_length=60, null=True)

    serial_number = models.CharField(max_length=60, null=True)
    # Here, we need a reference to a refundline in order to handle RMAs fully internally


class RMAState(ImmutableBlame):

    RMA_STATES = ('U', 'N', 'W', 'R', 'S', 'P', 'F', 'A', 'C')
    RMA_STATE_EXPLANATIONS = {'U': 'Untested', 'N': 'Not broken', 'W': 'Waiting for Number', 'R': 'Received Number',
                              'S': 'Sent', 'P': 'Replaced', 'F': 'Refunded by External', 'A': 'Abused by Customer',
                              'C': 'Returned to Customer'}


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
    OL_STATE_CHOICES = (('O','Ordered by Customer'),('L','Ordered at Supplier'),('A','Arrived at Store'),('C','Cancelled'),('S','Sold'))

    state = models.CharField(max_length=3, choices=OL_STATE_CHOICES)

    timestamp = models.DateTimeField(auto_now_add=True)

    orderline = models.ForeignKey('OrderLine')


class OrderLine(models.Model):
    # An order of a customer for a single product of a certain type
    order = models.ForeignKey(Order)

    wishable = models.ForeignKey(WishableType)

    state = models.CharField(max_length=3, choices=OrderLineState.OL_STATE_CHOICES)

    def get_type(self):
        return type(self)



from django.db import models
from crm.models import *
from article.models import *

# Create your models here.


class Order(models.Model):

    customer = Customer()

    date = models.DateTimeField(auto_created=True)

    copro = User()


class OrderLine():

    order = Order()

    # TODO: make articletype wishable
    wishable = ArticleType()

    def getType(self):
        if type(self) == ArticleType:


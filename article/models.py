from decimal import Decimal
from django.db import models
# from money.models import VAT
# Create your models here.
from money.models import SalesPrice, VAT


class ArticleType(models.Model):
    name = models.CharField(max_length=128)
    vat = models.ForeignKey(VAT)

    def __str__(self):
        return self.name

    def calculate_sales_price(self,cost):
        return SalesPrice(cost=cost.amount, vat=self.vat.vatrate,currency=cost.currency,amount=cost.amount*self.vat.vatrate*Decimal(1.085))

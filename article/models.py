from decimal import Decimal
from django.db import models
from money.models import SalesPrice
from register.models import AccountingGroup
from money.models import MoneyField


class WishableType(models.Model):

    name = models.CharField(max_length=255)

    # This abstract type can be ordered
    def save(self, *args, **kwargs):
        if type(self) == WishableType or type(self) == SellableType:
            raise AbstractClassInitializationError("Abstract class cannot be initialized")
        super(WishableType, self).save(*args, **kwargs)

    def get_name(self):
        return self.name

    def get_expected_sales_price(self):
        return None


class SellableType(WishableType):
    # This abstract type can be sold
    pass


class ArticleType(SellableType):
    # The type of an article you can put on a shelf
    fixed_price = MoneyField(null=True)

    accounting_group = models.ForeignKey(AccountingGroup)

    def __str__(self):
        return self.get_name()

    def get_vat(self):
        return self.accounting_group.vat_group.vatrate

    def calculate_sales_price(self, cost):
        return SalesPrice(cost=cost.amount, vat=self.accounting_group.vat_group.vatrate, currency=cost.currency,
                          amount=cost.amount * self.accounting_group.vat_group.vatrate * Decimal(1.085))

    def get_expected_sales_price(self):
        return None



class OrProductType(WishableType):
    # A choice between a number of ArticleTypes
    article_types = models.ManyToManyField(ArticleType)

    fixed_price = MoneyField(null=True)

    def get_expected_sales_price(self):
        return None


class AndProductType(SellableType):
    # A combination of ArticleTypes
    def get_expected_sales_price(self):
        return None


class ProductCombination(models.Model):
    # Helper class for the AndProductType. Has a number of ArticleTypes for inclusion in an AndProductType
    article_type = models.ForeignKey(ArticleType)

    amount = models.IntegerField()

    and_product = models.ForeignKey(AndProductType)

    def __str__(self):
        return "{}:{}x; Member of {}".format(self.article_type.name, self.amount, self.and_product.name)


class OtherCostType(SellableType):
    # Product that does not enter stock
    fixed_price = MoneyField()

    def get_sales_price(self):
        return self.fixed_price

    def get_name(self):
        return self.name

    def get_expected_sales_price(self):
        return self.get_sales_price()


class AbstractClassInitializationError(Exception):
    # Error when the system tries to save an abstract class
    pass

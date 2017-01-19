from decimal import Decimal

from django.db import models

from assortment.models import AssortmentLabel
from money.models import MoneyField, AccountingGroup, SalesPrice


class WishableType(models.Model):
    """
    General product type that can be desired by a customer. This type is product is not neccesarily sellable and does
    not exist as a type that our suppliers can provide. Ordering non-sellable types incurs significant logic in the
    system to resolve. Keep this in mind.
    """
    labels = models.ManyToManyField(AssortmentLabel)
    name = models.CharField(max_length=255)

    # This abstract type can be ordered
    def save(self, *args, **kwargs):
        if type(self) == WishableType or type(self) == SellableType:
            raise AbstractClassInitializationError("Abstract class cannot be initialized")
        super(WishableType, self).save(*args, **kwargs)

    def get_expected_sales_price(self):
        return None

    def __str__(self):
        return self.name

    class Meta:
        ordering = [
            'name',
        ]


class SellableType(WishableType):
    # This abstract type can be sold. Handling of these types in the system is quite easy.
    accounting_group = models.ForeignKey(AccountingGroup)

    def get_vat_group(self):
        return self.accounting_group.vat_group

    def get_vat_rate(self):
        return self.accounting_group.vat_group.vatrate


class ArticleType(SellableType):
    # The type of an article you can put on a shelf
    fixed_price = MoneyField(null=True)
    # The unique identifier around the world for this product. May also be an ISBN.
    ean = models.BigIntegerField(null=True)

    def calculate_sales_price(self, cost):
        return SalesPrice(amount=cost.amount * self.accounting_group.vat_group.vatrate * Decimal(1.085),
                          vat=self.accounting_group.vat_group.vatrate, currency=cost.currency, cost=cost.amount)

    def get_expected_sales_price(self):
        return None


class OrProductType(WishableType):
    # A choice between a number of ArticleTypes. At supplier ordering time, it is decided which ArticleType fulfills
    # the wish of the OrProductType
    article_types = models.ManyToManyField(ArticleType)

    fixed_price = MoneyField(null=True)

    def get_expected_sales_price(self):
        return None


class AndProductType(WishableType):
    # A combination of ArticleTypes
    pass

    def get_expected_sales_price(self):
        return None


class ProductCombination(models.Model):
    # Helper class for the AndProductType. Has a number of ArticleTypes for inclusion in an AndProductType
    article_type = models.ForeignKey(ArticleType)

    amount = models.IntegerField()

    and_product = models.ForeignKey(AndProductType)

    def __str__(self):
        return "{}:{}x; Member of {}".format(self.article_type.name, self.amount, self.and_product.name)

    class Meta:
        unique_together = ("article_type", "and_product")


class OtherCostType(SellableType):
    # Product that does not enter stock. This product is rarely physical.
    fixed_price = MoneyField()

    def get_sales_price(self):
        return self.fixed_price

    def get_expected_sales_price(self):
        return self.get_sales_price()


class AbstractClassInitializationError(Exception):
    # Error when the system tries to save an abstract class
    pass

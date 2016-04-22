from decimal import Decimal
from django.db import models
from money.models import SalesPrice, VAT, SalesPriceField
from supplier.models import Supplier
from register.models import AccountingGroup
from swipe.settings import DECIMAL_PLACES, MAX_DIGITS


class WishableType(models.Model):

    name = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if(not isinstance(self, OrProductType) and not isinstance(self, AndProductType)
           and not isinstance(self, ArticleType)
           and not isinstance(self, OtherCostType)):
            raise AbstractClassInitializationError("Abstract class cannot be initialized")
        super(WishableType, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class SellableType(WishableType, models.Model):

    has_fixed_price = models.BooleanField(default=False)

    book_keeping_group = models.ForeignKey(AccountingGroup)

    class Meta:
        abstract = True


class ArticleType(SellableType):

    suppliers = models.ManyToManyField(Supplier)

    #fixed_price = SalesPriceField()

    def __str__(self):
        return self.name

    def get_vat(self):
        return self.book_keeping_group.vat_group

    def calculate_sales_price(self,cost):
        return SalesPrice(cost=cost.amount, vat=self.vat.vatrate, currency=cost.currency,
                          amount=cost.amount * self.vat.vatrate * Decimal(1.085))


class OrProductType(WishableType, models.Model):

    article_types = models.ManyToManyField(ArticleType)


class AndProductType(SellableType):
    pass
    #fixed_price = SalesPriceField()


class ProductCombination(models.Model):

    article_type = models.ForeignKey(ArticleType)

    amount = models.IntegerField()

    and_product = models.ForeignKey(AndProductType)

    def __str__(self):
        return "{}:{}x; Member of {}".format(self.article_type.name,self.amount,self.and_product.name)


class OtherCostType(SellableType):
    price = SalesPrice

    #fixed_price = SalesPriceField()


class AbstractClassInitializationError(Exception):
    pass




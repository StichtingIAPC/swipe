from django.db import models
from blame.models import ImmutableBlame, Blame
from article.models import ArticleType
from money.models import CostField


class InternaliseDocument(Blame):
    """
    A way to use products for internal usage. Can be taken from any present article in the stockTable, including reesrved
    palces with a label like an order. The should be used for assigning products for internal usage and not as a magical
    way of reducing the stock.
    """
    # A memo which can contain the explanation for the usage of the products.
    memo = models.TextField()


class InternaliseLine(ImmutableBlame):
    """
    A line which contains the neccesary information about the products taken from stock. This is to be used as a way of
    logging products that are used for internal consumption.
    """
    # The articleType to be used
    article_type = models.ForeignKey(ArticleType)
    # The cost(excluding VAT) for using the product
    cost = CostField()
    # The labelType unique identifier to retrieve the product. Null for stock
    label_type = models.CharField(max_length=255, null=True)
    # If a labelType is used, this should be used(not Null, >0) to identify the StockLine. Null for stock.
    identifier = models.IntegerField(null=True)

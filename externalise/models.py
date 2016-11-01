from django.db import models
from blame.models import Blame, ImmutableBlame
from article.models import ArticleType
from money.models import CostField
from crm.models import User
from decimal import Decimal


class ExternaliseDocument(Blame):
    """
    A document that represents getting products from a non-standard source. Can be used to take in stock anything that is
    an articleType. Should not be used in place of supplier related processes as this method contains almost no information
    in describing the process. This is however quite useful for adding "random" products to stock.
    """

    memo = models.TextField()

    @staticmethod
    def create_external_products_document(user: User, article_information_list):
        """

        :param user: The user that created the document
        :param article_information_list: List(Tuple(article, count, cost)). A list of articles with multiplicity and cost.
        This is enough info to create the stock.
        """
        pass


class ExternaliseLine(ImmutableBlame):
    """
    The line that contains the history information. The products itself will enter stock.
    """

    article_type = models.ForeignKey(ArticleType)

    count = models.IntegerField()

    cost = CostField()

    def save(self, **kwargs):
        if not self.pk:
            if self.count > 0 and self.cost.amount >= Decimal(0):
                pass
            else:
                raise IncorrectStockDataError("Either stock is non-positive "
                                              "or cost is non-positive. Count: {}, Cost: {}".format(self.count, self.cost.amount))
        else:
            super(ExternaliseLine, self).save()


class IncorrectStockDataError(Exception):
    pass

from decimal import Decimal
from collections import defaultdict

from django.db import models, transaction

from blame.models import Blame, ImmutableBlame
from article.models import ArticleType
from money.models import CostField, Cost
from crm.models import User
from stock.models import StockChangeSet, StockLock, LockError
from tools.util import raiseif


class ExternaliseDocument(Blame):
    """
    A document that represents getting products from a non-standard source. Can be used to take in stock anything
    that is an articleType. Should not be used in place of supplier related processes as this method contains almost
    no information in describing the process. This is however quite useful for adding "random" products to stock.
    """
    # A memo that desribes why the externalisation process has taken place
    memo = models.TextField()

    @staticmethod
    @transaction.atomic
    def create_external_products_document(user: User, article_information_list, memo: str):
        """

        :param user: The user that created the document
        :param article_information_list: A list of articles with multiplicity and cost.
                                          This is enough info to create the stock.
        :type article_information_list: list(tuple(article, count, cost))
        :param memo: A memo to explain the reason for adding the articles
        """
        raiseif(not isinstance(user, User), IncorrectClassError())
        raiseif(not isinstance(memo, str), IncorrectClassError())
        raiseif(StockLock.is_locked(), LockError, "Stock is locked. Aborting.")

        counter = defaultdict(lambda: 0)
        for article, count, cost in article_information_list:
            raiseif(not isinstance(article, ArticleType), IncorrectClassError, "")
            raiseif(not isinstance(count, int), IncorrectClassError, "")
            raiseif(not isinstance(cost, Cost), IncorrectClassError, "")
            raiseif(count <= 0, IncorrectCountError, "Count is less than or equal to 0. This is not possible")
            # noinspection PyProtectedMember
            raiseif(cost._amount < Decimal(0), IncorrectPriceError,
                    "Products cost negative amount of money. This cannot happen.")
            counter[(article, cost)] += count

        stock_entries = []
        ext_lines = []
        for article, cost in counter.keys():
            stock_entries.append({'article': article,
                                  'book_value': cost,
                                  'count': counter[(article, cost)],
                                  'is_in': True})
            ext_lines.append(ExternaliseLine(article_type=article, count=counter[(article, cost)], cost=cost))

        # We constructed what we needed, now the saves
        doc = ExternaliseDocument(memo=memo, user_modified=user)
        doc.save()
        StockChangeSet.construct(description="Externalisation by document {}".format(doc.pk), entries=stock_entries,
                                 source=StockChangeSet.SOURCE_EXTERNALISE)
        for line in ext_lines:
            line.externalise_document = doc
            line.user_modified = user
            line.save(mod_stock=False)

        return doc


class ExternaliseLine(ImmutableBlame):
    """
    The line that contains the history information. The products itself will enter stock.
    """
    # The document to bundle line together
    externalise_document = models.ForeignKey(ExternaliseDocument, on_delete=models.PROTECT)
    # The article type to store in stock
    article_type = models.ForeignKey(ArticleType, on_delete=models.PROTECT)
    # The number of articles to store in stock
    count = models.IntegerField()
    # How much money each individual product costs
    cost = CostField()

    def save(self, mod_stock=True, **kwargs):
        if not self.pk:
            if mod_stock:
                if self.count > 0 and self.cost.amount >= Decimal(0):
                    entry = [
                        {'article': self.article_type,
                         'book_value': self.cost,
                         'count': self.count,
                         'is_in': True}
                    ]
                    StockChangeSet.construct(description="Direct externalisation from new externaliseline",
                                             entries=entry, source=StockChangeSet.SOURCE_EXTERNALISE)
                else:
                    raise IncorrectStockDataError("Either stock is non-positive or cost is non-positive. "
                                                  "Count: {}, Cost: {}".format(self.count, self.cost.amount))

        super(ExternaliseLine, self).save()

    def __str__(self):
        result = "Id: {}, Article Type: {}, Count: {}, Cost: {}".format(self.id, self.article_type_id, self.count,
                                                                        str(self.cost))
        return result


class IncorrectStockDataError(Exception):
    pass


class IncorrectCountError(Exception):
    pass


class IncorrectPriceError(Exception):
    pass


class IncorrectClassError(Exception):
    pass

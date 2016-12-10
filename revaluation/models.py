from django.db import models
from blame.models import ImmutableBlame, Blame
from article.models import ArticleType
from money.models import CostField, Cost
from crm.models import User
from tools.util import raiseif, raiseifnot
from stock.models import Stock
from stock.stocklabel import StockLabel


class RevaluationDocument(ImmutableBlame):
    """
    A document for revaluation. Contains lines with revaluation
    """
    # A memo indicating the reason why the products were revaluated(generally this is important)
    memo = models.CharField(max_length=255)

    @staticmethod
    def create_revaluation_document(user: User, article_type_cost_label_combinations):
        """
        Revalues a stockLine from its current price to a new price. Can be done to any line in the stock although
        it seems like that it will be done mostly for general unlabeled stockLines.
        :param user: The user that created the revaluation
        :param article_type_cost_label_combinations: List[Tuple[articleType, cost, labelType, labelKey]].
        Contains all the information to re-valuate. 'articleType' is the article from a stockLine that should be revalued
        'cost' is the new cost. In case of stock, both labelType and
        labelKey should be 'None'
        """
        raiseif(not isinstance(user, User), TypeError)
        revaluation_lines = []
        for article, cost, label_type, label_key in article_type_cost_label_combinations:
            raiseifnot(isinstance(article, ArticleType), TypeError, "article should be ArticleType")
            raiseifnot(isinstance(cost, Cost), TypeError, "cost should be Cost")
            raiseifnot(isinstance(label_type, StockLabel) or label_type is None, TypeError, "labelType should be StockLabel")
            raiseifnot(isinstance(label_key, int) or label_key is None, TypeError, "labelKey should be int")
            sts = Stock.objects.filter(article=article, labeltype=label_type, labelkey=label_key)
            if len(sts) > 1:
                raise FatalStockException(article, label_type, label_key, "If you read this, Stock probably broke "
                                                                          "horribly.")
            elif len(sts) == 0:
                raise NoStockExistsError("Cannot revalue since the article label combination does not exist")
            else:
                pass







    @staticmethod
    def create_revaluation_document_stock(user: User, article_type_cost_combination):
        """
        Has the same functionality as 'create_revaluation_document' but just for stock.
        :param user: The user that created the revaluation
        :param article_type_cost_combination: List[Tuple[articleType, cost]]. 'articleType' is the article from a stockLine that should be revalued
        'cost' is the new cost.
        """
        expanded_lines = []
        for article_type, cost in article_type_cost_combination:
            expanded_lines.append((article_type, cost, None, None))

        return RevaluationDocument.create_revaluation_document(user, expanded_lines)


class RevaluationLine(Blame):
    """
    A single line for revaluation. Contains all the information regarding the revaluation so it is useful for
    financial administrators.
    """
    # The document the line is going to be on
    revaluation_document = models.ForeignKey(RevaluationDocument)
    # The articleType in the stock
    article_type = models.ForeignKey(ArticleType)
    # Cost of the articleType before revaluation
    former_cost = CostField()
    # Cost after revaluation
    new_cost = CostField()
    # Number of articles that were revalued(all of that particular label)
    count = models.IntegerField()


class NoStockExistsError(Exception):
    pass


class FatalStockException(Exception):

    def __init__(self, article: ArticleType, label_type: StockLabel, label_key: int, text: str):
        self.article = article
        self.label_type = label_type
        self.label_key = label_key
        self.text = text

    def __str__(self):
        return self.text



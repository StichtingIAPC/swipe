from django.db import models
from blame.models import ImmutableBlame, Blame
from article.models import ArticleType
from money.models import CostField
from crm.models import User


class RevaluationDocument(ImmutableBlame):
    """
    A document for revaluation. Contains lines with revaluation
    """

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
        pass

    @staticmethod
    def create_revaluation_document_stock(user: User, article_type_cost_combination):
        """
        Has the same functionality as 'create_revaluation_document' but just for stock.
        :param user: The user that created the revaluation
        :param article_type_cost_combination: List[Tuple[articleType, cost]]. 'articleType' is the article from a stockLine that should be revalued
        'cost' is the new cost.
        """


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

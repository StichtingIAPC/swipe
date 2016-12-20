from django.db import models
from blame.models import Blame, ImmutableBlame
from article.models import ArticleType
from stock.models import StockChange


class StockCountDocument(ImmutableBlame):
    """
    The document collection all the counts of all the articles in the stock. The document is regarded as a diff
    from the previous stock count.
    """


class StockCountLine(Blame):
    """
    A line on a stock count. Considers all changes that have happened to an article since the last stock count.
    Registers the difference between the expected value and the real value by storing the expected number and
    the physical count of the product. The expected value is previous_count+in_count-out_count
    """

    # The article type
    article_type = models.ForeignKey(ArticleType)
    # The amount present at a previous count(or 0 if there was no previous count for this product)
    previous_count = models.IntegerField()
    # How much entered the system since the previous count
    in_count = models.IntegerField()
    # How much exited the system since the previous count
    out_count = models.IntegerField()
    # How much is actually present
    physical_count = models.IntegerField()


class TemporaryCounterLine:
    """
    A line that is presented to the user of a Stock count. Contains information generated from the database
    """

    article_type = ArticleType()

    previous_count = 0

    in_count = 0

    out_count = 0

    expected_count = 0

    @staticmethod
    def get_all_stock_changes_since_last_stock_count():
        if StockCountDocument.objects.exists():
            last_stock_count = StockCountDocument.objects.last()
            stock_changes = StockChange.objects.filter(
                change_set__date__gt=last_stock_count.date_created).select_related("change_set")
        else:
            stock_changes = StockChange.objects.all().select_related("change_set")

        return stock_changes

    @staticmethod
    def get_all_temporary_counterlines_since_last_stock_count():
        stock_changes = TemporaryCounterLine.get_all_stock_changes_since_last_stock_count()

        article_mods = {}
        # for change in stock_changes:
        #     if article_mods.get(change.article):
        #         pass
        #     else:
        #         pass

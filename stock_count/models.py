from django.db import models
from blame.models import Blame, ImmutableBlame
from article.models import ArticleType
from stock.models import StockChange
from time import timezone


class StockCountDocument(ImmutableBlame):
    """
    The document collection all the counts of all the articles in the stock. The document is regarded as a diff
    from the previous stock count.
    """

    def save(self, **kwargs):
        # To ensure setting the time, this should not be done by Django/database as it is not reliable when
        # precision matters in time calculation which are crucial to the process.
        self.date_created = timezone.now()
        super(StockCountDocument, self).save()


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

    def __init__(self, article_type, previous_count, in_count, out_count, expected_count):
        self.article_type = article_type
        self.previous_count = previous_count
        self.in_count = in_count
        self.out_count = out_count
        self.expected_count = expected_count

    def __str__(self):
        return "Article: {}, prev: {}, in: {}, out: {}, expected: {}".format(self.article_type, self.previous_count,
                                                                             self.in_count, self.out_count,
                                                                             self.expected_count)

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
    def get_all_provisional_temporary_counterlines(stock_changes):
        article_mods = {}
        for change in stock_changes:
            if article_mods.get(change.article):
                if change.is_in:
                    article_mods[change.article].in_count = article_mods[change.article].in_count + change.count
                else:
                    article_mods[change.article].out_count = article_mods[change.article].out_count + change.count
            else:
                if change.is_in:
                    article_mods[change.article] = TemporaryCounterLine(change.article, 0, change.count, 0, 0)
                else:
                    article_mods[change.article] = TemporaryCounterLine(change.article, 0, 0, change.count, 0)

    @staticmethod
    def get_all_temporary_counterlines_since_last_stock_count():
        pass
        #print(article_mods)


class TemporaryArticleCount(models.Model):
    """
    Temporary store of the article count. This allows for multiple users counting the stock separately.
    """
    # The articleType to be counted
    article_type = models.OneToOneField(ArticleType)
    # The number of articles counted temporarily.
    count = models.IntegerField()

    @staticmethod
    def clear_temporary_counts():
        """
        Sets all counts back to 0
        """
        TemporaryArticleCount.objects.all().update(count=0)

    @staticmethod
    def update_temporary_counts(article_type_count_combinations):
        """
        Generates a temporary store of article type counts. Persists until a count is completed.
        :param article_type_count_combinations: List[Tuple[ArticleType, int]] A number of articleTypes, which have
        a certain temporary count
        """
        # Not the fastest, fix by some smart fetching if this proves to be slow
        for article, count in article_type_count_combinations:
            art = TemporaryArticleCount.objects.filter(article_type=article)
            if len(art) == 0:
                TemporaryArticleCount.objects.create(article=article, count=count)
            else:
                art[0].count = count
                art[0].save()

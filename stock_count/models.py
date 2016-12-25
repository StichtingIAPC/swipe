from django.utils import timezone
from django.db import models
from blame.models import Blame, ImmutableBlame
from article.models import ArticleType
from stock.models import StockChange
from tools.util import raiseif


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

    @staticmethod
    def get_discrepancies():
        """
        This function is important to the stock count. It generates a list of function where the stored count is not
        equal to the expected count as in the TemporaryArticleCount for the article. This is needed because of the
        Stock-lines that articles can be taken from. When there is a shortage of items, you need to be able to pick
        the Stock-lines from which to subtract the articles. This function indicates where differences, if any, are.
        After this, you should be able to puzzle how to solve any stock shortage.
        """
        # In practice, the system should be more automatic and lenient. It will suffice for now.
        raiseif(ArticleType.objects.count() != TemporaryArticleCount.objects.filter(checked=True), UncountedError,
                "The number of ArticleTypes is not equal to the number of counted ArticleTypes")
        tacs = TemporaryArticleCount.objects.all()
        article_counts = {}
        for tac in tacs:
            article_counts[tac.article_type] = tac.count

        changes, stock_count = TemporaryCounterLine.get_all_stock_changes_since_last_stock_count()
        counter_lines = TemporaryCounterLine.\
            get_all_temporary_counterlines_since_last_stock_count(stock_changes=changes,
                                                                  last_stock_count=stock_count)
        discrepancies = []
        for line in counter_lines:
            article_type = line.article_type
            diff = article_counts[article_type] - line.expected_count
            if diff != 0:
                discrepancies.append((article_type, diff))

        return discrepancies


class StockCountLine(Blame):
    """
    A line on a stock count. Considers all changes that have happened to an article since the last stock count.
    Registers the difference between the expected value and the real value by storing the expected number and
    the physical count of the product. The expected value is previous_count+in_count-out_count
    """

    # The document which it
    document = models.ForeignKey(StockCountDocument)
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
    # NB: The expected count is 'previous_count + in_count - out_count' and this conforms to the database count


class TemporaryCounterLine:
    """
    A line that is presented to the user of a Stock count. Contains information generated from the database
    """

    article_type = ArticleType()

    previous_count = 0

    in_count = 0

    out_count = 0

    expected_count = 0

    def __init__(self, article_type, previous_count, in_count, out_count):
        self.article_type = article_type
        self.previous_count = previous_count
        self.in_count = in_count
        self.out_count = out_count
        self.expected_count = previous_count + in_count - out_count

    def __str__(self):
        return "Article: {}, prev: {}, in: {}, out: {}, expected: {}".format(self.article_type, self.previous_count,
                                                                             self.in_count, self.out_count,
                                                                             self.expected_count)

    def __eq__(self, other):
        if type(other) is not TemporaryCounterLine:
            return False
        else:
            return (self.article_type == other.article_type and self.previous_count == other.previous_count
            and self.in_count == other.in_count and self.out_count == other.out_count and self.expected_count ==
                    other.expected_count)

    @staticmethod
    def get_all_stock_changes_since_last_stock_count():
        if StockCountDocument.objects.exists():
            last_stock_count = StockCountDocument.objects.last()
            stock_changes = StockChange.objects.filter(
                change_set__date__gt=last_stock_count.date_created).select_related("change_set")
        else:
            last_stock_count = None
            stock_changes = StockChange.objects.all().select_related("change_set")

        return stock_changes, last_stock_count

    @staticmethod
    def get_all_temporary_counterlines_since_last_stock_count(stock_changes, last_stock_count: StockCountDocument):
        article_mods = {}
        for change in stock_changes:
            if article_mods.get(change.article):
                if change.is_in:
                    article_mods[change.article].in_count = article_mods[change.article].in_count + change.count
                else:
                    article_mods[change.article].out_count = article_mods[change.article].out_count + change.count
            else:
                if change.is_in:
                    article_mods[change.article] = TemporaryCounterLine(change.article, 0, change.count, 0)
                else:
                    article_mods[change.article] = TemporaryCounterLine(change.article, 0, 0, change.count)

        modded_articles = article_mods.keys()
        article_mods = list(article_mods.values())

        if last_stock_count:
            count_lines = StockCountLine.objects.filter(document=last_stock_count)
            count_dict = {}
            # Full the previous value as the expected value(DB value) at the previous count
            for line in count_lines:
                count_dict[line.article_type] = line.previous_count + line.in_count - line.out_count

            for mod in article_mods:
                count = count_dict.get(mod.article_type, None)
                if count:
                    mod.previous_count = count

        for mod in article_mods:  # Type: TemporaryCounterLine
            mod.expected_count = mod.previous_count + mod.in_count - mod.out_count

        return article_mods  # Type: List[TemporaryCounterLine]


class TemporaryArticleCount(models.Model):
    """
    Temporary store of the article count. This allows for multiple users counting the stock separately. Used as eventual
    input as the actual count.
    """
    # The articleType to be counted
    article_type = models.OneToOneField(ArticleType)
    # The number of articles counted temporarily.
    count = models.IntegerField()
    # Checks if the amount is truly counted or just a default.
    checked = models.BooleanField(default=False)

    @staticmethod
    def clear_temporary_counts():
        """
        Sets all counts back to 0
        """
        TemporaryArticleCount.objects.all().update(count=0, checked=False)

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
                TemporaryArticleCount.objects.create(article_type=article, count=count, checked=True)
            else:
                art[0].count = count
                art[0].save()

    def __str__(self):
        return "Article: {}, count: {}, checked: {}".format(self.article_type, self.count, self.checked)

    def __eq__(self, other):
        if type(other) is not TemporaryArticleCount:
            return False
        else:
            return self.article_type == other.article_type and self.count == other.count \
                   and self.checked == other.checked


class UncountedError(Exception):
    pass


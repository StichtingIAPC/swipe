from django.db import models
# Create your models here.
from django.db import transaction
from article.models import ArticleType
from money.models import CostField
from stock.exceptions import *
from money.exceptions import CurrencyInconsistencyError
from swipe.settings import ALLOW_NEGATIVE_STOCK


class Stock(models.Model):
    """
        Keeps track of the current state of the stock
        Do not edit this thing directly, use StockLog.log instead.

        article: What product is this line about?
        count: How many are in stock?
        book_value: What's the cost per product for this product?
    """
    article = models.ForeignKey(ArticleType)
    count = models.IntegerField()
    book_value = CostField()

    def save(self, *args, indirect=False, **kwargs):
        if not indirect:
            raise Id10TError(
                "Stock modifications shouldn't be done directly, but rather, they should be done on StockLog.")
        super(Stock, self).save(*args, **kwargs)

    @staticmethod
    def get_merge_line(mod):
        try:
            return Stock.objects.get(article=mod.article)
        except Stock.DoesNotExist:
            return None

    @staticmethod
    def modify(stock_mod):
        merge_line = Stock.get_merge_line(stock_mod)
        # Create new merge_line
        if not merge_line:
            merge_line = Stock(article=stock_mod.article, book_value=stock_mod.book_value, count=stock_mod.get_count())
        else:
            # Merge average book_value
            if merge_line.book_value.currency != stock_mod.book_value.currency:
                raise CurrencyInconsistencyError("GOT {} instead of {}".format(
                    merge_line.book_value.currency, stock_mod.book_value.currency))
            merge_cost_total = (merge_line.book_value * merge_line.count + stock_mod.book_value * stock_mod.get_count())
            merge_line.book_value = merge_cost_total / (stock_mod.get_count() + merge_line.count)

            # Update stockmod count
            merge_line.count += stock_mod.get_count()

        # TODO: Decide if we want this guard
        if merge_line.count < 0 and not ALLOW_NEGATIVE_STOCK:
            raise StockSmallerThanZeroError("Stock levels can't be below zero.")

        merge_line.save(indirect=True)
        return merge_line

    def __str__(self):
        return "{}| {}: {} @ {}".format(self.pk, self.article, self.count, self.book_value)


class StockLog(models.Model):
    """
    A log of one or multiple stock modifications
    """

    # When did the modification occur, will be automatically set to now.
    date = models.DateTimeField(auto_now_add=True)
    # Description of what happened
    description = models.CharField(max_length=255)

    @classmethod
    @transaction.atomic()
    def construct(cls, description, entries):
        """
        Construct a modification to the stock, and log it to the StockLog.
        :param description: A description of what happened
        :type description: str
        :param entries: A list of dictionaries with the data for the stock modifications. Each dictionary should have at least the keys "article", "count", "book_value" and "is_in". See StockModification.
        :type entries: list(dict)
        :return: A completed StockLog of the modification
        :rtype: StockLog
        """
        # Check if the entry dictionaries are complete
        for entry in entries:
            stock_modification_keys = ['article', 'count', 'book_value', 'is_in']

            if not all(key in entry.keys() for key in stock_modification_keys):
                raise ValueError("Missing data in StockLog entry values.\n"
                                 "Expected keys: {}\n"
                                 "Entry: {},\n"
                                 "StockLog description: {}".format(stock_modification_keys, entry, description))

        # Create the StockLog instance to use as a foreign key in the StockModifications
        sl = StockLog.objects.create(description=description)

        # Create the StockModifications and set the StockLog in them.
        for entry in entries:
            try:
                StockModification.objects.create(log_entry=sl, article=entry['article'], count=entry['count'], book_value=entry['book_value'], is_in=entry['is_in'])
            except ValueError as e:
                raise ValueError("Something went wrong while creating the a stock modification: {}".format(e))

        # Modify the stock for each StockModification now linked to the StockLog we created
        for modification in sl.stockmodification_set.all():
            Stock.modify(modification)

        # Return the created StockLog
        return sl


class StockModification(models.Model):
    """
        Log_entry: the Stocklog this Modification is a part of
        Article: What article is this StockModification a part of
        count: How many articles is this modification?
        book_value: What's the cost (per object) for this modification?
        is_in: Is this an in  (True) or an out (False)
    """
    log_entry = models.ForeignKey(StockLog)
    article = models.ForeignKey(ArticleType)
    count = models.IntegerField()
    book_value = CostField()
    is_in = models.BooleanField()

    def get_count(self):
        if self.is_in:
            return self.count
        else:
            return -1 * self.count

    def __str__(self):
        return "{}| {} x {}".format(self.pk, self.count, self.article)

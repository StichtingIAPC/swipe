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
        Do not edit this thing directly, use StockChangeSet.construct instead.

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
                "Stock modifications shouldn't be done directly, but rather, they should be done on StockChangeSet.")
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

        if merge_line.count < 0:
            raise StockSmallerThanZeroError("Stock levels can't be below zero.")

        merge_line.save(indirect=True)
        return merge_line

    def __str__(self):
        return "{}| {}: {} @ {}".format(self.pk, self.article, self.count, self.book_value)


class StockChangeSet(models.Model):
    """
    A log of one or multiple stock modifications
    """

    date = models.DateTimeField(auto_now_add=True)

    # Description of what happened
    memo = models.CharField(max_length=255, null=True)
    # Number to describe what caused this change
    enum = models.IntegerField()
    def save(self, *args, indirect=False, **kwargs):
        if not indirect:
            raise Id10TError(
                "Please use the StockChangeSet.construct function.")
        super(StockChangeSet, self).save(*args, **kwargs)

    @classmethod
    @transaction.atomic()
    def construct(cls, description, entries, enum):
        """
        Construct a modification to the stock, and log it to the StockChangeSet.
        :param description: A description of what happened
        :type description: str
        :param entries: A list of dictionaries with the data for the stock modifications. Each dictionary should have at least the keys "article", "count", "book_value" and "is_in". See StockChange.
        :type entries: list(dict)
        :return: A completed StockChangeSet of the modification
        :rtype: StockChangeSet
        """
        # Check if the entry dictionaries are complete
        for entry in entries:
            stock_modification_keys = ['article', 'count', 'book_value', 'is_in']

            if not all(key in entry.keys() for key in stock_modification_keys):
                raise ValueError("Missing data in StockChangeSet entry values.\n"
                                 "Expected keys: {}\n"
                                 "Entry: {},\n"
                                 "StockChangeSet description: {}".format(stock_modification_keys, entry, description))

        # Create the StockChangeSet instance to use as a foreign key in the Stockchanges
        sl = StockChangeSet(memo=description, enum=enum)
        sl.save(indirect=True)

        # Create the Stockchanges and set the StockChangeSet in them.
        for entry in entries:
            try:
                s = StockChange(change_set=sl, **entry)
                s.save(indirect=True)
            except ValueError as e:
                raise ValueError("Something went wrong while creating the a stock modification: {}".format(e))

        # Modify the stock for each StockChange now linked to the StockChangeSet we created
        for modification in sl.stockchange_set.all():
            Stock.modify(modification)

        # Return the created StockChangeSet
        return sl


class StockChange(models.Model):
    """
        Log_entry: the Stocklog this Modification is a part of
        change_set: What article is this StockChange a part of
        count: How many articles is this modification?
        book_value: What's the cost (per object) for this modification?
        is_in: Is this an in  (True) or an out (False)
        :date
    """
    change_set = models.ForeignKey(StockChangeSet)
    article = models.ForeignKey(ArticleType)
    count = models.IntegerField()
    book_value = CostField()
    is_in = models.BooleanField()
    memo = models.CharField(null=True, max_length=255)

    def save(self, *args, indirect=False, **kwargs):
        if not indirect:
            raise Id10TError(
                "Please use the StockChangeSet.construct function.")
        super(StockChange, self).save(*args, **kwargs)

    def get_count(self):
        if self.is_in:
            return self.count
        else:
            return -1 * self.count
    @property
    def date(self):
        return self.change_set.date
    def __str__(self):
        return "{}| {} x {}".format(self.pk, self.count, self.article)

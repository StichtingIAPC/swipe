from decimal import Decimal
from django.db import models
# Create your models here.
from django.db import transaction
from article.models import ArticleType
from money.models import SalesPriceField, SalesPrice, Cost, CostField


class Stock(models.Model):
    """
        Keeps track of the current state of the stock
        Do not edit this thing directly, use StockLog.log istead.

        article: What product is this line about?
        count: How many are in stock?
        salesprice: What's the salesprice for this product?
    """
    article = models.ForeignKey(ArticleType)
    count = models.IntegerField()
    cost = CostField()

    def save(self, indirect=False, *args, **kwargs):
        if not indirect and not kwargs.get("force_update", False):
            raise AssertionError(
                "Stock modifications shouldn't be done directly, but rather, they should be done on StockLog.")
        super(Stock, self).save(args, kwargs)

    @staticmethod
    def get_merge_line(mod):
        objects = Stock.objects.filter(article=mod.article)
        for obj in objects:
            return obj
        return None

    @staticmethod
    def modify(stock_mod, other_modifications):
        merge_line = Stock.get_merge_line(stock_mod)
        save = True
        # Check if it's already added this round
        if not merge_line:
            for mods in other_modifications:
                if mods.article == stock_mod.article:
                    merge_line = mods
                    save = False
        # Create new merge_line
        if not merge_line:
            print("HERE")
            if stock_mod.get_count() < 0:
                raise Exception("Stock levels can't be below zero.")
            merge_line = Stock(article=stock_mod.article, cost=stock_mod.cost, count=stock_mod.get_count())
        else:
            # Merge average cost
            merge_cost_total = (
                merge_line.cost.amount* merge_line.count + stock_mod.cost.amount * stock_mod.get_count())
            merge_line.cost = Cost(merge_cost_total / (stock_mod.get_count() + merge_line.count),
                              currency=merge_line.cost.currency)

            # Update stockmod count
            merge_line.count += stock_mod.get_count()

            # TODO: Decide if we want this guard
            if merge_line.count < 0:
                raise Exception("Stock levels can't be below zero.")

        merge_line.save(True)
        return merge_line

    def __str__(self):
        return (
            str(self.pk) + "|" + str(self.article) + "; Count: " + str(self.get_count()) + "; Price: " + str(self.salesprice))


class StockLog(models.Model):
    """
        date: When did this modification take place?
        description: please describe what happened here.
    """
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)

    @staticmethod
    @transaction.atomic
    def log(description, entries):
        # TODO: check negative stock
        sl = StockLog.objects.create(description=description)
        modifications = []
        for entry in entries:
            md = Stock.modify(entry, modifications)
            if md is not None:
                modifications.append(md)

        for entry in entries:
            entry.log_entry = sl
            entry.save()
        return sl


class StockModification(models.Model):
    """
        Log_entry: the Stocklog this Modification is a part of
        Article: What article is this Stockmodification a part of
        count: How many articles is this modification?
        is_in: Is this an in  (True) or an out (False)
    """
    log_entry = models.ForeignKey(StockLog)
    article = models.ForeignKey(ArticleType)
    count = models.IntegerField()
    cost = CostField()
    is_in = models.BooleanField()

    def get_count(self):
        if self.is_in:
            return self.count
        else:
            return -1*self.count

    def __str__(self):
        return str(self.pk) + ": " + str(self.count) + " x " + str(self.article)

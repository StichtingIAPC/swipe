from decimal import Decimal
from django.db import models
# Create your models here.
from django.db import transaction
from article.models import ArticleType
from money.models import SalesPriceField, SalesPrice, Cost


class Stock(models.Model):
    article = models.ForeignKey(ArticleType)
    count = models.IntegerField()
    salesprice = SalesPriceField()

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
                    save=False
        # Create new merge_line
        if not merge_line:
            merge_line = Stock(article=stock_mod.article, salesprice=stock_mod.salesprice, count=stock_mod.count)
        else:
            # Merge average cost
            merge_cost_total = (
                merge_line.salesprice.cost * merge_line.count + stock_mod.salesprice.cost * stock_mod.count)
            merge_cost = Cost(merge_cost_total / (stock_mod.count + merge_line.count), currency=merge_line.salesprice.currency)
            # Calculate new sales price based on the new cost.
            merge_line.salesprice = stock_mod.article.calculate_sales_price(merge_cost)

            # Update stockmod count
            merge_line.count += stock_mod.count

            # TODO: Decide if we want this guard
            if merge_line.count < 0:
                raise Exception("Stock levels can't be below zero.")
        merge_line.save(True)
        return merge_line

    def __str__(self):
        return (
            str(self.pk) + "|" + str(self.article) + "; Count: " + str(self.count) + "; Price: " + str(self.salesprice))


class StockLog(models.Model):
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
    log_entry = models.ForeignKey(StockLog)
    article = models.ForeignKey(ArticleType)
    count = models.IntegerField()
    salesprice = SalesPriceField()

    def __str__(self):
        return str(self.pk) + ": " + str(self.count) + " x " + str(self.article)

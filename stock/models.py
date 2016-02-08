from decimal import Decimal
from django.db import models
# Create your models here.
from django.db import transaction

from article.models import ArticleType
from money.models import SalesPriceField, SalesPrice


class Stock(models.Model):
    article = models.ForeignKey(ArticleType)
    count = models.IntegerField()
    salesprice = SalesPriceField()

    def save(self, indirect=False, **kwargs):
        if not indirect and not kwargs.get("force_update", False):
            raise AssertionError(
                "Stock modifications shouldn't be done directly, but rather, they should be done on StockLog.")
        super(Stock, self).save(self, kwargs)

    @staticmethod
    def get_merge_line(mod):
        objects = Stock.objects.filter(article=mod.article)
        for obj in objects:
            return obj
        return None

    @staticmethod
    def modify(stock_mod, other_modifications):
        merge_line = Stock.get_merge_line(stock_mod)
        if not merge_line:
            for mods in other_modifications:
                if mods.article == stock_mod.article:
                    merge_line = mods
        if not merge_line:
            merge_line = Stock(article=stock_mod.article, salesprice=stock_mod.salesprice, count=stock_mod.count)
        else:
            merge_cost_total = (
                merge_line.salesprice.cost * merge_line.count + stock_mod.salesprice.cost * stock_mod.count)
            merge_cost = merge_cost_total / (stock_mod.count + merge_line.count)
            # Todo: recalculate salesprice; check VAT's; check currencies
            merge_line.salesprice = SalesPrice(amount=Decimal(-1.0), currency=merge_line.salesprice.currency,
                                               vat=merge_line.salesprice.vat, cost=merge_cost)
            merge_line.count += stock_mod.count
            return None
        return merge_line

    def __str__(self):
        if self is None:
            return "Nonetype"
        return (
            str(self.pk) + "|" + str(self.article) + "; Count: " + str(self.count) + "; Price: " + str(self.salesprice))


class StockLog(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)

    @transaction.atomic
    def log(desc, entries):
        #TODO: check negative stock
        sl = StockLog.objects.create(description=desc)
        for entry in entries:
            entry.log_entry = sl
            entry.save()

        entries = StockModification.objects.filter(log_entry=sl.pk)
        modifications = []
        for entry in entries:
            md = Stock.modify(entry, modifications)
            if md is not None:
                modifications.append(md)
        for mod in modifications:
            mod.save(True)


class StockModification(models.Model):
    log_entry = models.ForeignKey(StockLog)
    article = models.ForeignKey(ArticleType)
    count = models.IntegerField()
    salesprice = SalesPriceField()

    def __str__(self):
        return str(self.pk) + ": " + str(self.count) + " x " + str(self.article)

from decimal import Decimal
from django.db import models
# Create your models here.
from article.models import ArticleType
from money.models import SalesPriceField, SalesPrice


class Stock(models.Model):
    article = models.ForeignKey(ArticleType)
    count = models.IntegerField()
    salesprice = SalesPriceField()

    def save(self,indirect=False, **kwargs):
        if not indirect:
            raise AssertionError("Stock modifications shouldn't be done directly, but rather, they should be done on StockLog.")
        super(Stock,self).save(self,**kwargs)

    def getMergeableLine(mod):
        objects = Stock.objects.filter(article=mod.article)
        for object in objects:
            return object
        return None

    def addModification(stockmod):
        mergeLine = Stock.getMergeableLine(stockmod)
        if not mergeLine:
            s = Stock(article=stockmod.article,salesprice=stockmod.salesprice,count=stockmod.count)
            s.save(True)
        else:
            mergeCost = (mergeLine.salesprice.cost*mergeLine.count+stockmod.salesprice.cost*stockmod.count)/(stockmod.count+mergeLine.count)
            mergeLine.salesprice=SalesPrice(amount=Decimal(-1.0),currency=mergeLine.salesprice.currency, vat=mergeLine.salesprice.vat,cost=mergeCost)
            mergeLine.count+= stockmod.count


class StockLog(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)

    def log(desc, entries):
        sl = StockLog.objects.create(description=desc)
        for entry in entries:
            entry.log_entry = sl
            entry.save()
        entries = StockModification.objects.filter(log_entry=sl.pk)
        for entry in entries:
            Stock.addModification(entry)


class StockModification(models.Model):
    log_entry = models.ForeignKey(StockLog)
    article = models.ForeignKey(ArticleType)
    count = models.IntegerField()
    salesprice = SalesPriceField()
from decimal import Decimal
from django.db import models
# Create your models here.
from article.models import ArticleType
from money.models import SalesPriceField, SalesPrice


class Stock(models.Model):
    article = models.ForeignKey(ArticleType)
    count = models.IntegerField()
    salesprice = SalesPriceField()

    def save(self, indirect=False,**kwargs):
        if not indirect:
            raise AssertionError("Stock modifications shouldn't be done directly, but rather, they should be done on StockLog.")
        super(Stock,self).__init__(self,**kwargs)

    def getMergeableLine(mod):
        objects = Stock.options.filter(article=mod.article)
        for object in objects:
            return object
        return None

    def addModification(stockmod):
        mergeLine = Stock.getMergeableLine(stockmod)
        if not mergeLine:
            Stock.save(indirect=True,article=stockmod.article,salesprice=stockmod.salesprice,count=stockmod.count)
        else:
            mergeCost = (mergeLine.salesPrice.cost*mergeLine.count+stockmod.salesprice.cost*stockmod.count)/(stockmod.count+mergeLine.count)
            mergeLine.salesprice=SalesPrice(amount=Decimal(-1.0),currency=mergeLine.salesprice.currency, vat=mergeLine.salesPrice.vat,cost=mergeCost)
            mergeLine.count+= stockmod.count


class StockLog(models.Model):
    date = models.DateTimeField()
    description = models.TextField()

    def save(self,**kwargs):
        super(StockLog,self).__init__(self,**kwargs)
        entries = StockModification.objects.filter(log_entry=self.pk)
        for entry in entries:
            Stock.addModification(entry)


class StockModification(models.Model):
    log_entry = models.ForeignKey(StockLog)
    article = models.ForeignKey(ArticleType)
    count = models.IntegerField()
    salesprice = SalesPriceField()
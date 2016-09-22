from django.contrib import admin

# Register your models here.
from stock.models import StockChange
from stock.models import StockChangeSet, Stock

admin.site.register(Stock)
admin.site.register(StockChange)
admin.site.register(StockChangeSet)

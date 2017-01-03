from django.db import models
from supplier.models import Supplier


class SupplierDataParser:
    pass


class XMLParser(SupplierDataParser):
    pass


class CSVParser(SupplierDataParser):
    pass


class XMLSupplierRelation(models.Model):

    supplier = models.ForeignKey(Supplier)

    # The descriptor for a product
    item_name = models.CharField(max_length=30)
    # Unique product identifier for supplier. Unique referer per supplier.
    number = models.CharField(max_length=30)

    name = models.CharField(max_length=30)

    price = models.CharField(max_length=30)

    supply = models.CharField(max_length=30)
    # EAN code. Unique referer globally.
    ean = models.CharField(max_length=30)

    minimum_order = models.CharField(max_length=30)

    packing_amount = models.CharField(max_length=30)


class CSVSupplierRelation(models.Model):

    supplier = models.ForeignKey(Supplier)

    # The element separator
    separator = models.CharField(max_length=5)

    start_at = models.IntegerField()
    # Unique product identifier for supplier. Unique referer per supplier.
    number = models.IntegerField()

    name = models.IntegerField()

    price = models.IntegerField()

    supply = models.IntegerField()
    # EAN code. Unique referer globally.
    ean = models.IntegerField()

    minimum_order = models.IntegerField()

    packing_amount = models.IntegerField()

from django.db import models
from supplier.models import Supplier


class SupplierDataParser:
    pass


class XMLParser(SupplierDataParser):
    pass


class CSVParser(SupplierDataParser):
    pass


class DataTypeSupplierRelation(models.Model):

    supplier = models.ForeignKey(Supplier)

class XMLSupplierRelation(DataTypeSupplierRelation):



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


class CSVSupplierRelation(DataTypeSupplierRelation):

    # The element separator
    separator = models.CharField(max_length=5)
    # The first line(s) can be CSV-metadata
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

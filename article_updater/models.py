from django.db import models
from supplier.models import Supplier
from tools.util import raiseifnot

import os.path
import mimetypes

import xml.etree.ElementTree as ET

class FileParser:

    @staticmethod
    def verify_file_exists(file_location: str) -> bool:
        raiseifnot(isinstance(file_location, str), TypeError)
        return os.path.isfile(file_location)

    @staticmethod
    def verify_file_is_plain_text(file_location: str) -> bool:
        raiseifnot(isinstance(file_location, str), TypeError)
        mimetype = mimetypes.guess_type(file_location)[0]  # type: str
        mimetype_first_part = mimetype.split('/')[0]
        return mimetype_first_part == 'text'


class SupplierDataParser:

    @staticmethod
    def parse(file_location):
        pass


class XMLParser(SupplierDataParser):

    @staticmethod
    def parse(file_location):
        raiseifnot(FileParser.verify_file_exists(file_location) and FileParser.verify_file_is_plain_text(file_location),
                   ParseError, "File is not an existing plain text file")
        try:
            result = ET.parse(file_location)
            return result
        except ET.ParseError:
            raise ParseError("File is not a valid XML file")


class CSVParser(SupplierDataParser):

    @staticmethod
    def parse(file_location):
        raiseifnot(FileParser.verify_file_exists(file_location) and FileParser.verify_file_is_plain_text(file_location),
                   ParseError, "File is not an existing plain text file")


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


class ParseError(Exception):
    pass

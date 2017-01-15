from django.db import models
from supplier.models import Supplier
from tools.util import raiseifnot

# For file lookup
import os.path
# For seeing that a file is plaintext-ish
import mimetypes

import xml.etree.ElementTree as ET

class FileParser:

    @staticmethod
    def verify_file_exists(file_location: str) -> bool:
        """
        Checks is a file exists
        :param file_location: A file path
        :return: The file at the file path exists.
        """
        raiseifnot(isinstance(file_location, str), TypeError)
        return os.path.isfile(file_location)

    @staticmethod
    def verify_file_is_plain_text(file_location: str) -> bool:
        """
        Contrary to the name, this function cannot actually check if a file is a plain text file.
        This function checks if it is likely that this file is parsable in a plain text manner.
        The intended purpose is to check if it can be parsed as a csv or xml type. The most reliable
        manner to do this is to use mimetypes. Unfortunately, there are several different mimetypes
        that may or not be plain text. The chosen algorithm therefore errors on the side of
        permissiveness and indicates that it's likely that a file is plain text. This function should
        be edited if there are more relevant documents that are plain text but which the function refuses
        to accept.
        :param file_location: A file path
        :return: The file at the path is probably plain text.
        """
        raiseifnot(isinstance(file_location, str), TypeError)
        mimetype = mimetypes.guess_type(file_location)[0]  # type: str
        mimetype_first_part = mimetype.split('/')[0]
        possible_correct_mimes = ['application/vnd.ms-excel', 'application/xml']
        return mimetype_first_part == 'text' or mimetype in possible_correct_mimes

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
    # The first line(s) can be CSV-metadata. The first line of a file is considered to be line 0.
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


class SupplierDataParser:
    pass


class XMLParser(SupplierDataParser):

    @staticmethod
    def parse(file_location, supplier_data: XMLSupplierRelation) -> ET.ElementTree:
        raiseifnot(FileParser.verify_file_exists(file_location) and FileParser.verify_file_is_plain_text(file_location),
                   SwipeParseError, "File is not an existing plain text file")
        # Can throw a ParseError
        result = ET.parse(file_location)
        return result


class CSVParser(SupplierDataParser):

    @staticmethod
    def parse(file_location, supplier_data: CSVSupplierRelation):
        raiseifnot(FileParser.verify_file_exists(file_location) and FileParser.verify_file_is_plain_text(file_location),
                   SwipeParseError, "File is not an existing plain text file")
        return CSVParser.parse_csv(file_location, supplier_data)

    @staticmethod
    def parse_csv(file_location, supplier_data: CSVSupplierRelation):
        if not FileParser.verify_file_exists(file_location) or not FileParser.verify_file_is_plain_text(file_location) \
                or mimetypes.guess_type(file_location)[0] in ['text/xml', 'application/xml']:
                    raise SwipeParseError("File is not a CSV file")
        file = open(file_location, 'r', encoding='utf-8')
        lines = file.readlines()
        element_lines = []
        for i in range(supplier_data.start_at, len(lines)):
            elements = lines[i].split(supplier_data.separator)
            for j in range(len(elements)):
                if elements[j].startswith('"') and elements[j].endswith('"'):
                    elements[j] = elements[j][1:-1]
            element_lines.append(elements)
        return element_lines


class SwipeParseError(Exception):
    pass

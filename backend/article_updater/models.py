from django.db import models
from supplier.models import Supplier
from tools.util import raiseifnot
from supplier.models import SupplierTypeArticle
from money.models import Cost
from decimal import Decimal

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
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)

    def verify_supplier_relation_integrity(self):
        pass


class XMLSupplierRelation(DataTypeSupplierRelation):
    # The xml identifier for a product
    item_name = models.CharField(max_length=30)
    # Unique product identifier for supplier. Unique referer per supplier.
    number = models.CharField(max_length=30)
    # The name given by the supplier
    name = models.CharField(max_length=30)
    # The first cost of the product
    cost = models.CharField(max_length=30)
    # How much the supplier has in stock
    supply = models.CharField(max_length=30)
    # EAN code. Unique referer globally.
    ean = models.CharField(max_length=30, null=True)
    # The minimum amount you have to buy
    minimum_order = models.CharField(max_length=30, null=True)
    # The divisor of the amount of products you have to buy
    packing_amount = models.CharField(max_length=30, null=True)

    def verify_supplier_relation_integrity(self):
        attrs = [self.item_name, self.number, self.name, self.cost, self.supply, self.ean, self.minimum_order,
                 self.packing_amount]
        name_set = set()
        for att in attrs:
            if att and att in name_set:
                raise SupplierRelationDataError("Attribute matched twice!")
            else:
                name_set.add(att)

    @staticmethod
    def get_supplier_type_articles(xml_data: ET, supplier_relation):
        """

        :param xml_data:
        :param supplier_relation:
        :type supplier_relation: XMLSupplierRelation
        :return:
        """
        supplier_type_articles = []
        for elem in xml_data.iter(supplier_relation.item_name):
            number = elem.find(supplier_relation.number).text
            name = elem.find(supplier_relation.name).text
            price_prep = elem.find(supplier_relation.cost).text  # type: str
            price_prep = price_prep.replace(",", ".")
            cost = Cost(amount=Decimal(price_prep), use_system_currency=True)
            supply = elem.find(supplier_relation.supply).text
            if supplier_relation.ean:
                ean = elem.find(supplier_relation.ean).text
                try:
                    ean = int(ean)
                except ValueError:
                    ean = -1
            else:
                ean = None
            if supplier_relation.minimum_order:
                minimum_order = int(elem.find(supplier_relation.minimum_order).text)
            else:
                minimum_order = None
            if supplier_relation.packing_amount:
                packing_amount = int(elem.find(supplier_relation.packing_amount).text)
            else:
                packing_amount = None
            supplier_type_articles.append(SupplierTypeArticle(number=number, name=name, cost=cost,
                                                              supply=supply, ean=ean,
                                                              minimum_number_to_order=minimum_order,
                                                              packing_amount=packing_amount,
                                                              supplier=supplier_relation.supplier))
        return supplier_type_articles


class CSVSupplierRelation(DataTypeSupplierRelation):
    # The element separator
    separator = models.CharField(max_length=5)
    # The first line(s) can be CSV-metadata. The first line of a file is considered to be line 0.
    start_at = models.IntegerField()
    # Unique product identifier for supplier. Unique referer per supplier.
    number = models.IntegerField()
    # The name given by the supplier
    name = models.IntegerField()
    # The first cost of the product
    cost = models.IntegerField()
    # How much the supplier has in stock
    supply = models.IntegerField()
    # EAN code. Unique referer globally.
    ean = models.IntegerField(null=True)
    # The minimum amount you have to buy
    minimum_order = models.IntegerField(null=True)
    # The divisor of the amount of products you have to buy
    packing_amount = models.IntegerField(null=True)

    def verify_supplier_relation_integrity(self):
        attrs = [self.separator, self.start_at, self.number, self.name, self.cost, self.supply, self.ean,
                 self.minimum_order,
                 self.packing_amount]
        name_set = set()
        for att in attrs:
            if att and att in name_set:
                raise SupplierRelationDataError("Attribute matched twice!")
            else:
                name_set.add(att)

    @staticmethod
    def get_supplier_type_articles(csv_data, supplier_relation):
        """

        :param csv_data:
        :param supplier_relation: The supplier location with the indices for the elements on the lines
        :type supplier_relation: CSVSupplierRelation
        :return:
        :rtype List[SupplierTypeArticle]
        """
        # Prevent indexes that go out of bounds
        max_col = -1
        positions = [supplier_relation.number, supplier_relation.name,
                     supplier_relation.cost, supplier_relation.supply, supplier_relation.ean,
                     supplier_relation.minimum_order, supplier_relation.packing_amount]
        for pos in positions:
            if pos is not None:
                max_col = max(max_col, pos)
        supplier_type_articles = []
        for line in csv_data:
            if len(line) >= max_col+1:
                number = line[supplier_relation.number]
                name = line[supplier_relation.name]
                cost_data = line[supplier_relation.cost]
                cost_data = cost_data.replace(",", ".")
                cost = Cost(amount=Decimal(cost_data), use_system_currency=True)
                supply = int(line[supplier_relation.supply])

                if supplier_relation.ean:
                    ean = line[supplier_relation.ean]
                    try:
                        ean = int(ean)
                    except ValueError:
                        ean = None
                else:
                    ean = None
                if supplier_relation.minimum_order:
                    minimum_order = int(line[supplier_relation.minimum_order])
                else:
                    minimum_order = None
                if supplier_relation.packing_amount:
                    packing_amount = int(line[supplier_relation.packing_amount])
                else:
                    packing_amount = None

                supplier_type_articles.append(SupplierTypeArticle(number=number, name=name, cost=cost,
                                                              supply=supply, ean=ean,
                                                              minimum_number_to_order=minimum_order,
                                                              packing_amount=packing_amount,
                                                              supplier=supplier_relation.supplier))
        return supplier_type_articles


class SupplierDataParser:
    @staticmethod
    def parse(file_location, supplier_data: DataTypeSupplierRelation):
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

        # The mode of the parser. Some CSV files can contain double and single quotes around their
        # elements. This means that the expected separator can appear freely in an element.
        # if this is the case, the parser needs to use a different separater(that is, with quotes)
        mode = 0
        first_line = lines[0]
        separators = [supplier_data.separator, "\"" + supplier_data.separator + "\"",
                      "'" + supplier_data.separator + "'"]
        separated = [0, 0, 0]
        for i in range(len(separators)):
            separated[i] = len(first_line.split(separators[i]))
        for i in range(len(separated)):
            if separated[i] >= separated[mode]:
                # Sets the mode to the highest amount of elements in a split with a certain
                # separator. It seems very likely that such an approach will yield the right
                # separator to be used
                mode = i

        # The elements to be parsed
        element_lines = []
        for i in range(supplier_data.start_at, len(lines)):
            elements = lines[i].split(separators[mode])
            if mode > 0:
                # Strip first single or double quote not separated
                elements[0] = elements[0][1:-1]
                # Strip last single or double quote
                elements[-1] = elements[-1][0:-2]
            element_lines.append(elements)
        return element_lines


class SwipeParseError(Exception):
    pass


class SupplierRelationDataError(Exception):
    pass

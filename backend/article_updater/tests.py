import mimetypes
from decimal import Decimal
from xml.etree.ElementTree import ParseError

from django.test import TestCase, SimpleTestCase

from article_updater.models import FileParser, XMLParser, CSVParser, \
    SwipeParseError, CSVSupplierRelation, XMLSupplierRelation, SupplierTypeArticle
from money.models import Cost
from supplier.models import Supplier
from tools.testing import allowFailure


class ParserTests(SimpleTestCase):

    def test_file_location_exists(self):
        self.assertTrue(FileParser.verify_file_exists("./article_updater/tests.py"))

    def test_file_location_does_not_exist(self):
        self.assertFalse(FileParser.verify_file_exists("./article_updater/ulaan_bator.py"))

    def test_xml_file_is_plain_text(self):
        file_location = "./article_updater/testing/Copaco_prijslijst_91658.xml"
        self.assertTrue(FileParser.verify_file_is_plain_text(file_location), mimetypes.guess_type(file_location)[0])

    @allowFailure(AttributeError)
    def test_csv_file_is_plain_text(self):
        file_location = "./article_updater/testing/nedis_csv_full.csv"
        self.assertTrue(FileParser.verify_file_is_plain_text(file_location), mimetypes.guess_type(file_location)[0])

    def test_file_is_not_plain_text(self):
        # I see what I did there
        self.assertFalse(FileParser.verify_file_is_plain_text("./article_updater/testing/PB145906.jpg"))

    @staticmethod
    def test_parsing_xml_does_not_error():
        file_location = "./article_updater/testing/Copaco_prijslijst_91658-brief.xml"
        XMLParser.parse(file_location, None)

    @allowFailure(AttributeError)
    def test_parsing_xml_from_csv_does_error(self):
        file_location = "./article_updater/testing/nedis_csv_brief.csv"
        with self.assertRaises(ParseError):
            XMLParser.parse(file_location, None)

    @staticmethod
    @allowFailure(AttributeError)
    def test_parsing_csv_does_not_error():
        file_location = "./article_updater/testing/nedis_csv_brief.csv"
        # noinspection PyUnusedLocal
        result = CSVParser.parse(file_location, CSVSupplierRelation(separator=",", start_at=1))

    def test_parsing_csv_from_xml_does_error(self):
        file_location = "./article_updater/testing/Copaco_prijslijst_91658-brief.xml"
        with self.assertRaises(SwipeParseError):
            # noinspection PyUnusedLocal
            result = CSVParser.parse(file_location, CSVSupplierRelation(separator=",", start_at=1))

    @allowFailure(AttributeError)
    def test_parsing_headless_file(self):
        file_location = "./article_updater/testing/nedis_csv_brief.csv"
        result = CSVParser.parse(file_location, CSVSupplierRelation(separator=",", start_at=1))
        self.assertEqual(3, len(result))
        self.assertEqual("CMP-CE039-1.5", result[0][2])
        self.assertEqual("CMP-CE070", result[1][2])
        self.assertEqual("CMP-CE070/3", result[2][2])


class SupplierTests(SimpleTestCase):
    """
    Actual supplier data. If this fails, either these tests are broken or importing will fail in real life.
    """

    def setUp(self):
        """
        Actual supplier data.
        """
        # Supplier dummies
        copaco_supplier = Supplier(pk=1)
        nedis_supplier = Supplier(pk=2)
        wave_supplier = Supplier(pk=3)
        # Supplier relation data, should work like the real suppliers
        self.copaco = XMLSupplierRelation(supplier=copaco_supplier, item_name="item", ean="EAN_code", number="item_id", name="long_desc",
                                          cost="price", supply="stock", minimum_order=None, packing_amount=None)
        self.nedis = CSVSupplierRelation(supplier=nedis_supplier, number=2, ean=6, name=9, cost=24, supply=32, minimum_order=28,
                                         packing_amount=None, start_at=1, separator=",")
        self.wave = CSVSupplierRelation(supplier=wave_supplier, number=0, ean=5, name=2, cost=3, supply=4, minimum_order=None,
                                        packing_amount=None, separator="|", start_at=1)

    def test_verify_supplier_relations(self):
        self.copaco.verify_supplier_relation_integrity()
        self.nedis.verify_supplier_relation_integrity()
        self.wave.verify_supplier_relation_integrity()

    @allowFailure(AttributeError)
    def test_verify_copaco(self):
        file_location = "./article_updater/testing/Copaco_prijslijst_91658-brief.xml"
        parsed = XMLParser.parse(file_location, self.copaco)
        root = parsed.getroot()
        self.assertEqual("ATE-0AD6-1705-26EG", root[0][0].text)

    @allowFailure(AttributeError)
    def test_verify_nedis(self):
        file_location = "./article_updater/testing/nedis_csv_brief.csv"
        parsed = CSVParser.parse(file_location, self.nedis)
        self.assertTrue(int, type(parsed[0][32]))

    @allowFailure(AttributeError)
    def test_verify_wave(self):
        file_location = "./article_updater/testing/wave-2017-01-02.csv"
        parsed = CSVParser.parse(file_location, self.wave)
        self.assertEqual("1N1AA006", parsed[0][0])

    @allowFailure(AttributeError)
    def test_produce_supplier_products_nedis(self):
        file_location = "./article_updater/testing/nedis_csv_brief.csv"
        parsed = CSVParser.parse(file_location, self.nedis)
        supplier_articles = CSVSupplierRelation.get_supplier_type_articles(parsed, self.nedis)
        # map of ean to supply level
        correct = {5412810134038: 730,
                   5412810102648: 611,
                   5412810102655: 732}
        for art in supplier_articles:
            self.assertEqual(art.supply, correct[art.ean])

    @allowFailure(AttributeError)
    def test_produce_supplier_products_wave(self):
        file_location = "./article_updater/testing/wave-2017-01-02.csv"
        parsed = CSVParser.parse(file_location, self.wave)
        supplier_articles = CSVSupplierRelation.get_supplier_type_articles(parsed, self.wave)
        # map of ean to supply level
        correct = {8717774650172: 1,
                   8717774650066: 6}
        for art in supplier_articles:
            self.assertEqual(art.supply, correct[art.ean])

    @allowFailure(AttributeError)
    def test_produce_supplier_products_copaco(self):
        file_location = "./article_updater/testing/Copaco_prijslijst_91658-brief.xml"
        parsed = XMLParser.parse(file_location, self.copaco)
        supplier_articles = XMLSupplierRelation.get_supplier_type_articles(parsed, self.copaco)
        correct = {"ATE-0AD6-1705-26EG": Cost(amount=Decimal("14.85"), use_system_currency=True),
                   "ATE-2L-1005P": Cost(amount=Decimal("20.16"), use_system_currency=True),
                   "ATE-2L-1010P": Cost(amount=Decimal("37.09"), use_system_currency=True)
                   }
        for art in supplier_articles:
            self.assertEqual(art.cost, correct[art.number])

    @allowFailure(AttributeError)
    def test_process_nedis_full(self):
        file_location = "./article_updater/testing/nedis_csv_full.csv"
        parsed = CSVParser.parse(file_location, self.nedis)
        # noinspection PyUnusedLocal
        supplier_articles = CSVSupplierRelation.get_supplier_type_articles(parsed, self.nedis)
        self.assertEqual(len(supplier_articles), 9657)
        # Checks if the extraction does not fail

    def test_process_copaco_full(self):
        # Not actually the complete copaco list but a subset of its articles
        file_location = "./article_updater/testing/Copaco_prijslijst_91658.xml"
        parsed = XMLParser.parse(file_location, self.copaco)
        # noinspection PyUnusedLocal
        supplier_articles = XMLSupplierRelation.get_supplier_type_articles(parsed, self.copaco)
        self.assertEqual(len(supplier_articles), 317)
        # Checks if the extraction does not fail


class DatabaseParserTests(TestCase):

    def setUp(self):
        wave_supplier = Supplier(name="Wave")
        wave_supplier.save()
        self.wave = CSVSupplierRelation(supplier=wave_supplier, number=0, ean=5, name=2, cost=3, supply=4,
                                        minimum_order=None,
                                        packing_amount=None, separator="|", start_at=1)

    @allowFailure(AttributeError)
    def test_ean_has_full_precision(self):
        file_location = "./article_updater/testing/wave-2017-01-02.csv"
        parsed = CSVParser.parse(file_location, self.wave)
        supplier_articles = CSVSupplierRelation.get_supplier_type_articles(parsed, self.wave)
        for sa in supplier_articles:
            sa.save()
        retrieved = SupplierTypeArticle.objects.get(number="1N1AA006")
        self.assertEqual(retrieved.ean, 8717774650172)
        self.assertEqual(retrieved.cost, Cost(amount=Decimal("5.1"), use_system_currency=True))

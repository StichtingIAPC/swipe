from django.test import TestCase, SimpleTestCase
from xml.etree.ElementTree import ParseError
from article_updater.models import FileParser, XMLParser, CSVParser, \
    SwipeParseError, CSVSupplierRelation, XMLSupplierRelation
import mimetypes


class ParserTests(SimpleTestCase):

    def test_file_location_exists(self):
        self.assertTrue(FileParser.verify_file_exists("./article_updater/tests.py"))

    def test_file_location_does_not_exist(self):
        self.assertFalse(FileParser.verify_file_exists("./article_updater/ulaan_bator.py"))

    def test_xml_file_is_plain_text(self):
        file_location = "./article_updater/testing/Copaco_prijslijst_91658.xml"
        self.assertTrue(FileParser.verify_file_is_plain_text(file_location), mimetypes.guess_type(file_location)[0])

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

    def test_parsing_xml_from_csv_does_error(self):
        file_location = "./article_updater/testing/nedis_csv_brief.csv"
        with self.assertRaises(ParseError):
            XMLParser.parse(file_location, None)

    @staticmethod
    def test_parsing_csv_does_not_error():
        file_location = "./article_updater/testing/nedis_csv_brief.csv"
        result = CSVParser.parse(file_location, CSVSupplierRelation(separator=",", start_at=1))

    def test_parsing_csv_from_xml_does_error(self):
        file_location = "./article_updater/testing/Copaco_prijslijst_91658-brief.xml"
        with self.assertRaises(SwipeParseError):
            result = CSVParser.parse(file_location, CSVSupplierRelation(separator=",", start_at=1))

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
        self.copaco = XMLSupplierRelation(item_name="item", ean="EAN_code", number="item_id", name="long_desc",
                                          price="price", supply="stock", minimum_order=None, packing_amount=None)
        self.nedis = CSVSupplierRelation(number=2, ean=6, name=11, price=24, supply=32, minimum_order=28,
                                         packing_amount=None, start_at=1, separator=",")
        self.wave = CSVSupplierRelation(number=0, ean=0, name=2, price=3, supply=4, minimum_order=None,
                                        packing_amount=None, separator="|", start_at=1)

    def test_verify_supplier_relations(self):
        self.copaco.verify_supplier_relation_integrity()
        self.nedis.verify_supplier_relation_integrity()
        self.wave.verify_supplier_relation_integrity()

    def test_verify_copaco(self):
        file_location = "./article_updater/testing/Copaco_prijslijst_91658-brief.xml"
        parsed = XMLParser.parse(file_location, self.copaco)
        root = parsed.getroot()
        self.assertEqual("ATE-0AD6-1705-26EG", root[0][0].text)

    def test_verify_nedis(self):
        file_location = "./article_updater/testing/nedis_csv_brief.csv"
        parsed = CSVParser.parse(file_location, self.nedis)
        self.assertTrue(int, type(parsed[0][32]))

    def test_verify_wave(self):
        file_location = "./article_updater/testing/wave-2017-01-02.csv"
        parsed = CSVParser.parse(file_location, self.wave)
        self.assertEqual("1N1AA006", parsed[0][0])


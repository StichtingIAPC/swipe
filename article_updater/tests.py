from django.test import TestCase, SimpleTestCase
from article_updater.models import FileParser


class ParserTests(SimpleTestCase):

    def test_file_location_exists(self):
        self.assertTrue(FileParser.verify_file_exists("./article_updater/tests.py"))

    def test_file_location_does_not_exist(self):
        self.assertFalse(FileParser.verify_file_exists("./article_updater/ulaan_bator.py"))

    # This should work but doesn't. Finding out why might be difficult due to different
    # computers giving different answers.
    def test_xml_file_is_plain_text(self):
        self.assertTrue(FileParser.verify_file_is_plain_text("./article_updater/testing/Copaco_prijslijst_91658.xml"))

    def test_csv_file_is_plain_text(self):
        pass

    def test_file_is_not_plain_text(self):
        # I see what I did there
        self.assertFalse(FileParser.verify_file_is_plain_text("./article_updater/testing/PB145906.jpg"))


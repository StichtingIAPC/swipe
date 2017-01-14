from django.test import TestCase, SimpleTestCase
from article_updater.models import FileParser


class ParserTests(SimpleTestCase):

    def test_file_location_exists(self):
        self.assertTrue(FileParser.verify_file_exists("./article_updater/tests.py"))

    def test_file_location_does_not_exist(self):
        self.assertFalse(FileParser.verify_file_exists("./article_updater/ulaan_bator.py"))

    def test_file_is_plain_text(self):
        self.assertTrue(FileParser.verify_file_is_plain_text("./article_updater/tests.py"))

    def test_file_is_not_plain_text(self):
        # If this test fails, it means that the file in question has been moved or deleted.
        # In that case, either delete this test or point it to a different file.
        # This file was chosen because at the time, it was one of the few plaintext files
        # in the repository.
        self.assertFalse(FileParser.verify_file_is_plain_text("./www/static/scss/www/foundation-icons/"
                                                              "foundation-icons.eot"))


from django.test import TestCase
from tools.testing import TestData
from supplier.models import SupplierTypeArticle


class SupplierTypeArticleUpdaterTests(TestCase, TestData):

    def setUp(self):
        self.setup_base_data()

    def test_insertion_of_new_lines(self):
        sta1 = SupplierTypeArticle()
        stas = []  # type: list[SupplierTypeArticle]



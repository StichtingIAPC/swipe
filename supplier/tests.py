from django.test import TestCase
from tools.testing import TestData
from supplier.models import SupplierTypeArticle, SupplierTypeArticleProcessingError


class SupplierTypeArticleUpdaterTests(TestCase, TestData):

    def setUp(self):
        self.setup_base_data()

    def test_insertion_of_new_lines(self):
        sta1 = SupplierTypeArticle()
        stas = []  # type: list[SupplierTypeArticle]


    def test_mixing_suppliers_does_not_work(self):
        sta1 = SupplierTypeArticle(supplier=self.supplier_1)
        sta2 = SupplierTypeArticle(supplier=self.supplier_2)
        stas = [sta1, sta2]
        with self.assertRaises(SupplierTypeArticleProcessingError):
            SupplierTypeArticle.process_supplier_type_articles(stas)





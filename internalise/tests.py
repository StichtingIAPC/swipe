from django.test import TestCase
from tools.testing import TestData
from logistics.models import StockWish
from internalise.models import InternaliseDocument, InternaliseLine
from stock.models import Stock

class InternaliseTests(TestCase, TestData):

    def setUp(self):
        self.setup_base_data()

    def test_creation_function_stock_single_article(self):
        StockWish.create_stock_wish(user_modified=self.user_1, articles_ordered=[[self.articletype_1, 20], [self.articletype_2, 20]])
        self.create_suporders(article_1=5)
        self.create_packingdocuments(article_1=4)
        st = Stock.objects.get(article=self.articletype_1, labeltype__isnull=True)
        IN_STOCK = 4
        self.assertEqual(st.count, IN_STOCK)
        cost = st.book_value
        INTERNALISE_ART_1 = 2
        InternaliseDocument.create_internal_products_document(user=self.user_1,
                                                              articles_with_information=[(self.articletype_1, INTERNALISE_ART_1, None, None)],
                                                              memo="Foo")
        st = Stock.objects.get(article=self.articletype_1, labeltype__isnull=True)
        self.assertEqual(st.count, IN_STOCK-INTERNALISE_ART_1)
        doc = InternaliseDocument.objects.get()
        self.assertEqual(doc.memo, "Foo")
        line = InternaliseLine.objects.get()
        self.assertEqual(line.internalise_document, doc)
        self.assertEqual(line.cost, cost)
        self.assertEqual(line.article_type, self.articletype_1)
        self.assertFalse(line.label_type)
        self.assertFalse(line.identifier)
        self.assertEqual(line.count, INTERNALISE_ART_1)

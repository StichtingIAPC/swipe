from django.test import TestCase
from tools.testing import TestData
from logistics.models import StockWish
from internalise.models import InternaliseDocument, InternaliseLine, DataValidityError
from stock.models import Stock
from stock.stocklabel import OrderLabel
from order.models import OrderLine


class InternaliseTests(TestCase, TestData):

    def setUp(self):
        self.setup_base_data()

    def test_creation_function_stock_single_article(self):
        StockWish.create_stock_wish(user_modified=self.user_1, articles_ordered=[[self.articletype_1, 20],
                                                                                 [self.articletype_2, 20]])
        self.create_suporders(article_1=5)
        self.create_packingdocuments(article_1=4)
        st = Stock.objects.get(article=self.articletype_1, labeltype__isnull=True)
        IN_STOCK = 4
        self.assertEqual(st.count, IN_STOCK)
        cost = st.book_value
        INTERNALISE_ART_1 = 2
        InternaliseDocument.create_internal_products_document(user=self.user_1,
                                                              articles_with_information=[(self.articletype_1,
                                                                                          INTERNALISE_ART_1,
                                                                                          None, None)],
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

    def test_creation_function_stock_two_articles(self):
        IN_STOCK_ART_1 = 6
        IN_STOCK_ART_2 = 5
        self.create_stockwish(article_1=IN_STOCK_ART_1, article_2=IN_STOCK_ART_2)
        self.create_suporders(article_1=IN_STOCK_ART_1, article_2=IN_STOCK_ART_2)
        self.create_packingdocuments(article_1=IN_STOCK_ART_1, article_2=IN_STOCK_ART_2)

        st_1 = Stock.objects.get(article=self.articletype_1)
        st_2 = Stock.objects.get(article=self.articletype_2)

        self.assertEqual(st_1.count, IN_STOCK_ART_1)
        self.assertEqual(st_2.count, IN_STOCK_ART_2)

        INTERN_ART_1 = 3
        INTERN_ART_2 = 4

        cost_1 = st_1.book_value
        cost_2 = st_2.book_value
        InternaliseDocument.create_internal_products_document(user=self.user_1,
                                                              articles_with_information=[
                                                                  (self.articletype_1, INTERN_ART_1, None, None),
                                                                  (self.articletype_2, INTERN_ART_2, None, None)],
                                                              memo="Foo2")
        doc = InternaliseDocument.objects.get()
        self.assertEqual(InternaliseLine.objects.count(), 2)
        il_1 = InternaliseLine.objects.get(article_type=self.articletype_1)
        il_2 = InternaliseLine.objects.get(article_type=self.articletype_2)
        self.assertEqual(il_1.cost, cost_1)
        self.assertEqual(il_2.cost, cost_2)
        self.assertEqual(il_1.internalise_document, doc)
        self.assertEqual(il_2.internalise_document, doc)
        self.assertEqual(il_1.count, INTERN_ART_1)
        self.assertEqual(il_2.count, INTERN_ART_2)
        self.assertFalse(il_1.label_type)
        self.assertFalse(il_1.identifier)
        self.assertFalse(il_2.label_type)
        self.assertFalse(il_2.identifier)

    def test_creation_function_mixed(self):
        IN_STOCK_ART_1 = 6
        CUST_ORDER_1 = 5
        self.create_stockwish(article_1=IN_STOCK_ART_1, article_2=0)
        order = self.create_custorders(article_1=CUST_ORDER_1, article_2=0)
        self.create_suporders(article_1=IN_STOCK_ART_1+CUST_ORDER_1, article_2=0)
        self.create_packingdocuments(article_1=IN_STOCK_ART_1+CUST_ORDER_1, article_2=0)
        st_1 = Stock.objects.get(labeltype__isnull=True)
        st_2 = Stock.objects.get(labeltype="Order")
        cost_1 = st_1.book_value
        cost_2 = st_2.book_value
        self.assertEqual(st_1.count, IN_STOCK_ART_1)
        self.assertEqual(st_2.count, CUST_ORDER_1)

        INTERN_ART_1 = 3
        INTERN_ART_2 = 4
        ols = OrderLine.objects.filter(state='A', wishable__sellabletype__articletype=self.articletype_1)
        self.assertEqual(len(ols), CUST_ORDER_1)

        InternaliseDocument.create_internal_products_document(user=self.user_1,
                                                              articles_with_information=[
                                                                  (self.articletype_1, INTERN_ART_1, None, None),
                                                                  (self.articletype_1, INTERN_ART_2, OrderLabel, order.id)],
                                                              memo="Foo2")
        st_1 = Stock.objects.get(labeltype__isnull=True)
        self.assertEqual(st_1.count, IN_STOCK_ART_1-INTERN_ART_1)
        st_2 = Stock.objects.get(labeltype="Order")
        self.assertEqual(st_2.count, CUST_ORDER_1-INTERN_ART_2)
        doc = InternaliseDocument.objects.get()
        self.assertEqual(InternaliseLine.objects.count(), 2)
        il_1 = InternaliseLine.objects.get(article_type=self.articletype_1, label_type__isnull=True)
        il_2 = InternaliseLine.objects.get(article_type=self.articletype_1, label_type__isnull=False)
        self.assertEqual(il_1.cost, cost_1)
        self.assertEqual(il_2.cost, cost_2)
        self.assertEqual(il_1.internalise_document, doc)
        self.assertEqual(il_2.internalise_document, doc)
        self.assertEqual(il_1.count, INTERN_ART_1)
        self.assertEqual(il_2.count, INTERN_ART_2)
        self.assertFalse(il_1.label_type)
        self.assertFalse(il_1.identifier)
        self.assertEqual(il_2.label_type, "Order")
        self.assertEqual(il_2.identifier, order.id)

        ols = OrderLine.objects.filter(state='A', wishable__sellabletype__articletype=self.articletype_1)
        self.assertEqual(len(ols), CUST_ORDER_1-INTERN_ART_2)

    def test_just_enough_articles(self):
        IN_STOCK_ART_1 = 6
        self.create_stockwish(article_1=IN_STOCK_ART_1, article_2=0)
        self.create_suporders(article_1=IN_STOCK_ART_1, article_2=0)
        self.create_packingdocuments(article_1=IN_STOCK_ART_1, article_2=0)
        st = Stock.objects.get()
        self.assertEqual(st.count, IN_STOCK_ART_1)
        InternaliseDocument.create_internal_products_document(user=self.user_1,
                                                              articles_with_information=[
                                                                  [self.articletype_1, IN_STOCK_ART_1, None, None]
                                                              ],
                                                              memo="Foo3")
        stock = Stock.objects.all()
        self.assertEqual(len(stock), 0)

    def test_just_enough_articles_labeled(self):
        CUST_ORDERED_ART_1 = 6
        order = self.create_custorders(article_1=CUST_ORDERED_ART_1, article_2=0, othercost_1=0, othercost_2=0)
        self.create_suporders(article_1=CUST_ORDERED_ART_1, article_2=0)
        self.create_packingdocuments(article_1=CUST_ORDERED_ART_1, article_2=0)
        st = Stock.objects.get()
        self.assertEqual(st.count, CUST_ORDERED_ART_1)
        ols = OrderLine.objects.filter(state='A')
        self.assertEqual(len(ols), CUST_ORDERED_ART_1)
        InternaliseDocument.create_internal_products_document(user=self.user_1,
                                                              articles_with_information=[
                                                                  [self.articletype_1, CUST_ORDERED_ART_1,
                                                                   OrderLabel, order.id]],
                                                              memo="Foo3")
        stock = Stock.objects.all()
        self.assertEqual(len(stock), 0)
        ols = OrderLine.objects.filter(state='I')
        self.assertEqual(len(ols), CUST_ORDERED_ART_1)

    def test_too_many_articles_labeled(self):
        CUST_ORDERED_ART_1 = 6
        order = self.create_custorders(article_1=CUST_ORDERED_ART_1, article_2=0)
        self.create_suporders(article_1=CUST_ORDERED_ART_1, article_2=0)
        self.create_packingdocuments(article_1=CUST_ORDERED_ART_1, article_2=0)
        st = Stock.objects.get()
        self.assertEqual(st.count, CUST_ORDERED_ART_1)
        with self.assertRaises(DataValidityError):
            InternaliseDocument.create_internal_products_document(user=self.user_1,
                                                                  articles_with_information=[
                                                                      [self.articletype_1, CUST_ORDERED_ART_1+1,
                                                                       OrderLabel, order.id]],
                                                                  memo="Foo3")

    def test_too_many_articles_labeled_loose(self):
        CUST_ORDERED_ART_1 = 6
        order = self.create_custorders(article_1=CUST_ORDERED_ART_1, article_2=0)
        self.create_suporders(article_1=CUST_ORDERED_ART_1, article_2=0)
        self.create_packingdocuments(article_1=CUST_ORDERED_ART_1, article_2=0)
        st = Stock.objects.get()
        self.assertEqual(st.count, CUST_ORDERED_ART_1)
        with self.assertRaises(DataValidityError):
            InternaliseDocument.create_internal_products_document(user=self.user_1,
                                                                  articles_with_information=[
                                                                   [self.articletype_1, CUST_ORDERED_ART_1-2,
                                                                    OrderLabel, order.id],
                                                                   [self.articletype_1, 3, OrderLabel, order.id]],
                                                                  memo="Foo3")

    def test_too_many_articles_stock(self):
        CUST_ORDERED_ART_1 = 6
        self.create_stockwish(article_1=CUST_ORDERED_ART_1, article_2=0)
        self.create_suporders(article_1=CUST_ORDERED_ART_1, article_2=0)
        self.create_packingdocuments(article_1=CUST_ORDERED_ART_1, article_2=0)
        st = Stock.objects.get()
        self.assertEqual(st.count, CUST_ORDERED_ART_1)
        with self.assertRaises(DataValidityError):
            InternaliseDocument.create_internal_products_document(user=self.user_1,
                                                                  articles_with_information=[
                                                                   [self.articletype_1, CUST_ORDERED_ART_1+1,
                                                                    None, None]],
                                                                  memo="Foo3")

    def test_too_many_articles_stock_loose(self):
        CUST_ORDERED_ART_1 = 6
        self.create_stockwish(article_1=CUST_ORDERED_ART_1, article_2=0)
        self.create_suporders(article_1=CUST_ORDERED_ART_1, article_2=0)
        self.create_packingdocuments(article_1=CUST_ORDERED_ART_1, article_2=0)
        st = Stock.objects.get()
        self.assertEqual(st.count, CUST_ORDERED_ART_1)
        with self.assertRaises(DataValidityError):
            InternaliseDocument.create_internal_products_document(user=self.user_1,
                                                                  articles_with_information=[
                                                                   [self.articletype_1, CUST_ORDERED_ART_1-2,
                                                                    None, None],
                                                                   [self.articletype_1, 3, None, None]],
                                                                  memo="Foo3")

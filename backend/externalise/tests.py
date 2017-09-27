from django.test import TestCase
from tools.testing import TestData
from decimal import Decimal
from money.models import Cost
from externalise.models import ExternaliseDocument, IncorrectPriceError, IncorrectCountError
from stock.models import Stock


class ExternaliseTests(TestCase, TestData):

    def setUp(self):
        self.setup_base_data()

    def test_illegal_cost(self):
        local_cost = Cost(amount=Decimal(-2), currency=self.currency_eur)
        count = 2
        with self.assertRaises(IncorrectPriceError):
            ExternaliseDocument.create_external_products_document(user=self.user_1,
                                                                  article_information_list=[
                                                                      (self.articletype_1, count, local_cost)],
                                                                  memo="Foo")

    def test_zero_count(self):
        local_cost = Cost(amount=Decimal(2), currency=self.currency_eur)
        count = 0
        with self.assertRaises(IncorrectCountError):
            ExternaliseDocument.create_external_products_document(user=self.user_1,
                                                                  article_information_list=[
                                                                      (self.articletype_1, count, local_cost)],
                                                                  memo="Foo")

    def test_single_article(self):
        local_cost = Cost(amount=Decimal(2), currency=self.currency_eur)
        count = 2
        ExternaliseDocument.create_external_products_document(user=self.user_1,
                                                              article_information_list=[
                                                                  [self.articletype_1, count, local_cost]],
                                                              memo="Foo")
        st = Stock.objects.get()
        self.assertEqual(st.book_value, local_cost)
        self.assertEqual(st.count, count)
        self.assertEqual(st.article, self.articletype_1)
        self.assertEqual(st.labeltype, None)

    def test_article_combination_merging(self):
        local_cost = Cost(amount=Decimal(2), currency=self.currency_eur)
        count = 2
        ExternaliseDocument.create_external_products_document(user=self.user_1,
                                                              article_information_list=[
                                                                  [self.articletype_1, count, local_cost],
                                                                  [self.articletype_1, count, local_cost]],
                                                              memo="Foo")
        st = Stock.objects.get()
        self.assertEqual(st.book_value, local_cost)
        self.assertEqual(st.count, 2*count)
        self.assertEqual(st.article, self.articletype_1)
        self.assertEqual(st.labeltype, None)

    def test_separate_addition_of_article(self):
        local_cost = Cost(amount=Decimal(2), currency=self.currency_eur)
        count = 2
        ExternaliseDocument.create_external_products_document(user=self.user_1,
                                                              article_information_list=[
                                                                  [self.articletype_1, count, local_cost],
                                                                  ],
                                                              memo="Foo")
        ExternaliseDocument.create_external_products_document(user=self.user_1,
                                                              article_information_list=[
                                                                  [self.articletype_1, count, local_cost],
                                                              ],
                                                              memo="Foo")
        st = Stock.objects.get()
        self.assertEqual(st.book_value, local_cost)
        self.assertEqual(st.count, 2 * count)
        self.assertEqual(st.article, self.articletype_1)
        self.assertEqual(st.labeltype, None)

    def test_two_articles(self):
        local_cost_1 = Cost(amount=Decimal(4), currency=self.currency_eur)
        local_cost_2 = Cost(amount=Decimal(5), currency=self.currency_eur)
        count_1 = 2
        count_2 = 3
        ExternaliseDocument.create_external_products_document(user=self.user_1,
                                                              article_information_list=[
                                                                  [self.articletype_1, count_1, local_cost_1],
                                                                  [self.articletype_2, count_2, local_cost_2]],
                                                              memo="Foo")
        self.assertEqual(len(Stock.objects.all()), 2)
        st_1 = Stock.objects.get(article=self.articletype_1)
        st_2 = Stock.objects.get(article=self.articletype_2)
        self.assertEqual(st_1.book_value, local_cost_1)
        self.assertEqual(st_1.count, count_1)
        self.assertEqual(st_1.article, self.articletype_1)
        self.assertEqual(st_1.labeltype, None)
        self.assertEqual(st_2.book_value, local_cost_2)
        self.assertEqual(st_2.count, count_2)
        self.assertEqual(st_2.article, self.articletype_2)
        self.assertEqual(st_2.labeltype, None)

    def test_price_merging(self):
        local_cost_1 = Cost(amount=Decimal(2), currency=self.currency_eur)
        local_cost_2 = Cost(amount=Decimal(5), currency=self.currency_eur)
        count_1 = 2
        count_2 = 1
        ExternaliseDocument.create_external_products_document(user=self.user_1,
                                                              article_information_list=[
                                                                  [self.articletype_1, count_1, local_cost_1]],
                                                              memo="Foo")
        ExternaliseDocument.create_external_products_document(user=self.user_1,
                                                              article_information_list=[
                                                                  [self.articletype_1, count_2, local_cost_2]],
                                                              memo="Foo2")
        desired_cost = Cost(amount=Decimal(3), currency=self.currency_eur)
        st = Stock.objects.get()
        self.assertEqual(st.book_value, desired_cost)
        self.assertEqual(st.count, count_1+count_2)
        self.assertEqual(st.article, self.articletype_1)
        self.assertEqual(st.labeltype, None)

from django.test import TestCase
from tools.testing import TestData
from revaluation.models import RevaluationDocument, NoStockExistsError, RevaluationLine, CostError
from stock.models import StockChangeSet, Stock
from stock.stocklabel import OrderLabel
from money.models import Cost
from decimal import Decimal


class RevaluationTests(TestCase, TestData):

    def setUp(self):
        self.setup_base_data()

    def test_revaluation_of_non_existent_general_stock(self):
        stock_addition = []
        stock_addition.append({"article": self.articletype_2,
                               "book_value": self.cost_eur_1,
                               "count": 5,
                               "is_in": True})
        StockChangeSet.construct(description="Test", entries=stock_addition, enum=0)
        with self.assertRaises(NoStockExistsError):
            RevaluationDocument.create_revaluation_document(user=self.user_1,article_type_cost_label_combinations=[(self.articletype_1, self.cost_eur_1, None, None)], memo="")

    def test_revaluation_of_wrong_label_stock(self):
        stock_addition = []
        stock_addition.append({"article": self.articletype_2,
                               "book_value": self.cost_eur_1,
                               "count": 5,
                               "is_in": True,
                               "label": OrderLabel(1)})
        StockChangeSet.construct(description="Test", entries=stock_addition, enum=0)
        with self.assertRaises(NoStockExistsError):
            RevaluationDocument.create_revaluation_document(user=self.user_1, article_type_cost_label_combinations=[
                (self.articletype_1, self.cost_eur_1, None, None)], memo="")

    def test_revaluation_single_general_stock_line(self):
        stock_addition = []
        COUNT = 5
        stock_addition.append({"article": self.articletype_1,
                               "book_value": self.cost_eur_1,
                               "count": COUNT,
                               "is_in": True})
        StockChangeSet.construct(description="Test", entries=stock_addition, enum=0)
        RevaluationDocument.create_revaluation_document(user=self.user_1,
                                                        article_type_cost_label_combinations=[(self.articletype_1, self.cost_eur_2, None, None)],
                                                        memo="")
        reval_doc = RevaluationDocument.objects.get()
        reval_line = RevaluationLine.objects.get()
        self.assertEqual(reval_line.revaluation_document, reval_doc)
        self.assertEqual(reval_line.former_cost, self.cost_eur_1)
        self.assertEqual(reval_line.new_cost, self.cost_eur_2)
        self.assertEqual(reval_line.count, COUNT)
        self.assertEqual(reval_line.article_type, self.articletype_1)

    def test_revaluation_of_labeled_stock(self):
        stock_addition = []
        COUNT = 5
        stock_addition.append({"article": self.articletype_1,
                               "book_value": self.cost_eur_1,
                               "count": COUNT,
                               "is_in": True,
                               "label": OrderLabel(1)})
        StockChangeSet.construct(description="Test", entries=stock_addition, enum=0)
        RevaluationDocument.create_revaluation_document(user=self.user_1,
                                                        article_type_cost_label_combinations=[
                                                            (self.articletype_1, self.cost_eur_2, OrderLabel, 1)],
                                                        memo="")
        reval_doc = RevaluationDocument.objects.get()
        reval_line = RevaluationLine.objects.get()
        self.assertEqual(reval_line.revaluation_document, reval_doc)
        self.assertEqual(reval_line.former_cost, self.cost_eur_1)
        self.assertEqual(reval_line.new_cost, self.cost_eur_2)
        self.assertEqual(reval_line.count, COUNT)
        self.assertEqual(reval_line.article_type, self.articletype_1)

    def test_revaluation_multiple_stocks(self):
        stock_addition = []
        COUNT_1 = 5
        COUNT_2 = 3
        stock_addition.append({"article": self.articletype_1,
                               "book_value": self.cost_eur_1,
                               "count": COUNT_1,
                               "is_in": True,
                               })
        stock_addition.append({"article": self.articletype_2,
                               "book_value": self.cost_eur_3,
                               "count": COUNT_2,
                               "is_in": True,
                               })
        StockChangeSet.construct(description="Test", entries=stock_addition, enum=0)
        RevaluationDocument.create_revaluation_document(user=self.user_1,
                                                        article_type_cost_label_combinations=[
                                                            (self.articletype_1, self.cost_eur_2, None, None),
                                                            (self.articletype_2, self.cost_eur_4, None, None)],
                                                        memo="")
        reval_doc = RevaluationDocument.objects.get()
        reval_line = RevaluationLine.objects.all()
        self.assertEqual(len(reval_line), 2)
        if reval_line[0].article_type == self.articletype_1:
            reval_1 = reval_line[0]
            reval_2 = reval_line[1]
        else:
            reval_1 = reval_line[1]
            reval_2 = reval_line[0]
        self.assertEqual(reval_1.revaluation_document, reval_doc)
        self.assertEqual(reval_1.former_cost, self.cost_eur_1)
        self.assertEqual(reval_1.new_cost, self.cost_eur_2)
        self.assertEqual(reval_1.count, COUNT_1)
        self.assertEqual(reval_1.article_type, self.articletype_1)

        self.assertEqual(reval_2.revaluation_document, reval_doc)
        self.assertEqual(reval_2.former_cost, self.cost_eur_3)
        self.assertEqual(reval_2.new_cost, self.cost_eur_4)
        self.assertEqual(reval_2.count, COUNT_2)
        self.assertEqual(reval_2.article_type, self.articletype_2)

    def test_shorthand_stock_method(self):
        stock_addition = []
        COUNT_1 = 5
        COUNT_2 = 3
        stock_addition.append({"article": self.articletype_1,
                               "book_value": self.cost_eur_1,
                               "count": COUNT_1,
                               "is_in": True,
                               })
        stock_addition.append({"article": self.articletype_2,
                               "book_value": self.cost_eur_3,
                               "count": COUNT_2,
                               "is_in": True,
                               })
        StockChangeSet.construct(description="Test", entries=stock_addition, enum=0)
        RevaluationDocument.create_revaluation_document_stock(user=self.user_1,
                                                              article_type_cost_combination=[
                                                            (self.articletype_1, self.cost_eur_2)
                                                            ],
                                                        memo="")

        reval_doc = RevaluationDocument.objects.get()
        reval_line = RevaluationLine.objects.get()
        self.assertEqual(reval_line.revaluation_document, reval_doc)
        self.assertEqual(reval_line.former_cost, self.cost_eur_1)
        self.assertEqual(reval_line.new_cost, self.cost_eur_2)
        self.assertEqual(reval_line.count, COUNT_1)
        self.assertEqual(reval_line.article_type, self.articletype_1)

    def test_negative_price(self):
        stock_addition = []
        stock_addition.append({"article": self.articletype_2,
                               "book_value": self.cost_eur_1,
                               "count": 5,
                               "is_in": True})
        StockChangeSet.construct(description="Test", entries=stock_addition, enum=0)
        with self.assertRaises(CostError):
            RevaluationDocument.create_revaluation_document(user=self.user_1, article_type_cost_label_combinations=[
                (self.articletype_1, Cost(amount=Decimal(-3.14), currency=self.currency_eur), None, None)], memo="")

    def test_one_article_multiple_labels(self):
        stock_addition = []
        COUNT_1 = 5
        COUNT_2 = 3
        stock_addition.append({"article": self.articletype_1,
                               "book_value": self.cost_eur_1,
                               "count": COUNT_1,
                               "is_in": True,
                               })
        stock_addition.append({"article": self.articletype_1,
                               "book_value": self.cost_eur_3,
                               "count": COUNT_2,
                               "is_in": True,
                               "label": OrderLabel(1)
                               })
        StockChangeSet.construct(description="Test", entries=stock_addition, enum=0)
        RevaluationDocument.create_revaluation_document(user=self.user_1,
                                                        article_type_cost_label_combinations=[
                                                            (self.articletype_1, self.cost_eur_2, None, None),
                                                            ],
                                                        memo="")
        reval_doc = RevaluationDocument.objects.get()
        reval_line = RevaluationLine.objects.get()
        self.assertEqual(reval_line.revaluation_document, reval_doc)
        self.assertEqual(reval_line.former_cost, self.cost_eur_1)
        self.assertEqual(reval_line.new_cost, self.cost_eur_2)
        self.assertEqual(reval_line.count, COUNT_1)
        self.assertEqual(reval_line.article_type, self.articletype_1)
        # Assure no change in labeled stock
        st = Stock.objects.get(article=self.articletype_1, labeltype=OrderLabel.labeltype)
        self.assertEqual(st.book_value, self.cost_eur_3)





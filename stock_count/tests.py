from django.test import TestCase
from tools.testing import TestData
from stock_count.models import TemporaryCounterLine, StockCountDocument
from stock.models import Stock, StockChangeSet

class PreparationTests(TestCase, TestData):

    def setUp(self):
        self.setup_base_data()

    def test_stock_changes_no_stock_modifications(self):
        changes = TemporaryCounterLine.get_all_stock_changes_since_last_stock_count()
        print(changes)
        self.assertEqual(len(changes), 0)

    def test_temporary_count_line_no_stock_count(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_eur_1,
                  'count': 5,
                  'is_in': True},
                 {'article': self.articletype_1,
                  'book_value': self.cost_eur_1,
                  'count': 7,
                  'is_in': True}
                 ]
        StockChangeSet.construct(description="", entries=entry, enum=0)
        changes = TemporaryCounterLine.get_all_stock_changes_since_last_stock_count()
        print(changes)

    def test_temporary_count_line_one_stock_count_no_new_lines(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_eur_1,
                  'count': 5,
                  'is_in': True},
                 {'article': self.articletype_1,
                  'book_value': self.cost_eur_1,
                  'count': 7,
                  'is_in': True}
                 ]
        StockChangeSet.construct(description="", entries=entry, enum=0)
        StockCountDocument(user_modified=self.user_1).save()
        changes = TemporaryCounterLine.get_all_stock_changes_since_last_stock_count()

        print(changes)

    def test_temporary_count_line_one_stock_count_some_new_lines(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_eur_1,
                  'count': 5,
                  'is_in': True},
                 {'article': self.articletype_1,
                  'book_value': self.cost_eur_1,
                  'count': 7,
                  'is_in': True}
                 ]
        StockChangeSet.construct(description="", entries=entry, enum=0)
        StockCountDocument(user_modified=self.user_1).save()
        entry = [{'article': self.articletype_2,
                  'book_value': self.cost_eur_2,
                  'count': 5,
                  'is_in': True},
                 ]
        StockChangeSet.construct(description="", entries=entry, enum=0)
        changes = TemporaryCounterLine.get_all_stock_changes_since_last_stock_count()

        print(changes)


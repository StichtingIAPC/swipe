from django.test import TestCase
from tools.testing import TestData
from stock_count.models import TemporaryCounterLine, StockCountDocument, StockCountLine, TemporaryArticleCount
from stock.models import Stock, StockChangeSet
import time


class PreparationTests(TestCase, TestData):

    def setUp(self):
        self.setup_base_data()

    def test_stock_changes_no_stock_modifications(self):
        changes, stock_count = TemporaryCounterLine.get_all_stock_changes_since_last_stock_count()
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
        changes, stock_count = TemporaryCounterLine.get_all_stock_changes_since_last_stock_count()
        self.assertEqual(len(changes), 2)

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
        changes, stock_count = TemporaryCounterLine.get_all_stock_changes_since_last_stock_count()

        self.assertEqual(len(changes), 0)

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
        # This prevents the next StockChange from being stores at the exact time as the StockCountDocument
        time.sleep(0.01)
        StockChangeSet.construct(description="", entries=entry, enum=0)
        changes, stock_count = TemporaryCounterLine.get_all_stock_changes_since_last_stock_count()
        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0].article, self.articletype_2)
        self.assertEqual(changes[0].count, 5)

    def test_temporary_counter_lines_no_previous_stock_counts(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_eur_1,
                  'count': 5,
                  'is_in': True},
                 {'article': self.articletype_1,
                  'book_value': self.cost_eur_1,
                  'count': 7,
                  'is_in': True}
                 , {'article': self.articletype_1,
                  'book_value': self.cost_eur_1,
                  'count': 3,
                  'is_in': False},
                 {'article': self.articletype_2,
                  'book_value': self.cost_eur_2,
                  'count': 11,
                  'is_in': True},
                 {'article': self.articletype_2,
                  'book_value': self.cost_eur_2,
                  'count': 7,
                  'is_in': True},
                 {'article': self.articletype_2,
                  'book_value': self.cost_eur_2,
                  'count': 2,
                  'is_in': False}
                 ]
        StockChangeSet.construct(description="", entries=entry, enum=0)
        changes, count = TemporaryCounterLine.get_all_stock_changes_since_last_stock_count()
        mods = TemporaryCounterLine.get_all_temporary_counterlines_since_last_stock_count(changes, count)
        for mod in mods:
            if mod.article_type == self.articletype_1:
                correct = TemporaryCounterLine(self.articletype_1, 0, 12, 3)
                self.assertEqual(mod, correct, "{} not equal to {}".format(mod, correct))
            elif mod.article_type == self.articletype_2:
                correct = TemporaryCounterLine(self.articletype_2, 0, 18, 2)
                self.assertEqual(mod, correct, "{} not equal to {}".format(mod, correct))
            else:
                raise (AssertionError("Wrong articleType"))

    def test_temporary_counter_lines_one_stock_change(self):
        IN_1 = 5
        IN_2 = 7
        IN_TOTAL = IN_1 + IN_2
        OUT_1 = 3
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_eur_1,
                  'count': IN_1,
                  'is_in': True},
                 {'article': self.articletype_1,
                  'book_value': self.cost_eur_1,
                  'count': IN_2,
                  'is_in': True},
                  {'article': self.articletype_1,
                   'book_value': self.cost_eur_1,
                   'count': OUT_1,
                   'is_in': False},
                 ]
        StockChangeSet.construct(description="", entries=entry, enum=0)
        sc = StockCountDocument(user_created=self.user_1)
        sc.save()
        scl = StockCountLine(document=sc, article_type=self.articletype_1, previous_count=0, in_count=12,
                       out_count=3, physical_count=9, user_modified=sc.user_created)
        scl.save()
        NEW_IN_1 = 1
        NEW_IN_2 = 2
        NEW_IN_TOTAL = NEW_IN_1 + NEW_IN_2
        NEW_OUT_1 = 4
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_eur_1,
                  'count': NEW_IN_1,
                  'is_in': True},
                 {'article': self.articletype_1,
                  'book_value': self.cost_eur_1,
                  'count': NEW_IN_2,
                  'is_in': True},
                 {'article': self.articletype_1,
                  'book_value': self.cost_eur_1,
                  'count': NEW_OUT_1,
                  'is_in': False},
                 ]
        StockChangeSet.construct(description="", entries=entry, enum=0)
        changes, count = TemporaryCounterLine.get_all_stock_changes_since_last_stock_count()
        mods = TemporaryCounterLine.get_all_temporary_counterlines_since_last_stock_count(changes, count)
        correct = TemporaryCounterLine(self.articletype_1, IN_TOTAL-OUT_1, NEW_IN_TOTAL, NEW_OUT_1)
        self.assertEqual(mods[0], correct)

    def test_temporary_counter_lines_newly_used_article(self):
        IN_1 = 5
        IN_2 = 7
        IN_TOTAL = IN_1 + IN_2
        OUT_1 = 3
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_eur_1,
                  'count': IN_1,
                  'is_in': True},
                 {'article': self.articletype_1,
                  'book_value': self.cost_eur_1,
                  'count': IN_2,
                  'is_in': True},
                 {'article': self.articletype_1,
                  'book_value': self.cost_eur_1,
                  'count': OUT_1,
                  'is_in': False},
                 ]
        StockChangeSet.construct(description="", entries=entry, enum=0)
        sc = StockCountDocument(user_created=self.user_1)
        sc.save()
        scl = StockCountLine(document=sc, article_type=self.articletype_1, previous_count=0, in_count=12,
                             out_count=3, physical_count=9, user_modified=sc.user_created)
        scl.save()
        NEW_IN_1 = 1
        NEW_IN_2 = 2
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_eur_1,
                  'count': NEW_IN_1,
                  'is_in': True},
                 {'article': self.articletype_2,
                  'book_value': self.cost_eur_1,
                  'count': NEW_IN_2,
                  'is_in': True},
                 ]
        StockChangeSet.construct(description="", entries=entry, enum=0)
        changes, count = TemporaryCounterLine.get_all_stock_changes_since_last_stock_count()
        mods = TemporaryCounterLine.get_all_temporary_counterlines_since_last_stock_count(changes, count)
        correct = {self.articletype_1: TemporaryCounterLine(self.articletype_1, IN_TOTAL-OUT_1,
                                                            NEW_IN_1, 0,),
                   self.articletype_2: TemporaryCounterLine(self.articletype_2, 0, NEW_IN_2, 0)}
        for mod in mods:
            self.assertEqual(mod, correct.get(mod.article_type))


class IntermediaryTests(TestCase, TestData):

    def setUp(self):
        self.setup_base_data()

    def test_store_temporary_count(self):
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 4), (self.articletype_2, 8)])
        correct = {self.articletype_1: TemporaryArticleCount(article_type=self.articletype_1, count=4, checked=True),
                   self.articletype_2: TemporaryArticleCount(article_type=self.articletype_2, count=8, checked=True)}
        tacs = TemporaryArticleCount.objects.all()
        for tac in tacs:
            self.assertEqual(tac, correct.get(tac.article_type))

    def test_reuse_temporary_count(self):
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 4), (self.articletype_2, 8)])
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 5)])
        correct = {self.articletype_1: TemporaryArticleCount(article_type=self.articletype_1, count=5, checked=True),
                   self.articletype_2: TemporaryArticleCount(article_type=self.articletype_2, count=8, checked=True)}
        tacs = TemporaryArticleCount.objects.all()
        for tac in tacs:
            self.assertEqual(tac, correct.get(tac.article_type))

    def test_reset_temporary_count(self):
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 4), (self.articletype_2, 8)])
        TemporaryArticleCount.clear_temporary_counts()
        correct = {self.articletype_1: TemporaryArticleCount(article_type=self.articletype_1, count=0, checked=False),
                   self.articletype_2: TemporaryArticleCount(article_type=self.articletype_2, count=0, checked=False)}
        tacs = TemporaryArticleCount.objects.all()
        for tac in tacs:
            self.assertEqual(tac, correct.get(tac.article_type))


class EndingTests(TestCase, TestData):

    def setUp(self):
        self.setup_base_data()

    def test_get_discrepancies_not_enough_counts(self):
        TemporaryArticleCount.update_temporary_counts([(self.ar)])


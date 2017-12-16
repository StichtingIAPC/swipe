import time
from decimal import Decimal

from django.test import TestCase

from article.models import ArticleType
from money.models import Cost
from order.models import Order, OrderLine
from stock.models import Stock, StockChangeSet
from stock.stocklabel import OrderLabel
from stock_count.models import TemporaryCounterLine, StockCountDocument, StockCountLine, TemporaryArticleCount, \
    UncountedError, SolutionError, DiscrepancySolution
from tools.testing import TestData


class PreparationTests(TestCase, TestData):
    def setUp(self):
        # It is essential that the number of articleTypes does not diverge. Because of this, articleTypes
        # are saved in a fixed manner
        self.part_setup_vat_group()
        self.part_setup_currency()
        self.part_setup_accounting_group()
        self.part_setup_costs()
        self.part_setup_supplier()
        self.articletype_1 = ArticleType(name="ArticleType 1", accounting_group=self.accounting_group_components)
        self.articletype_1.save()
        self.articletype_2 = ArticleType(name="ArticleType 2", accounting_group=self.accounting_group_food)
        self.articletype_2.save()
        self.part_setup_users()

    def test_stock_changes_no_stock_modifications(self):
        changes, stock_count = TemporaryCounterLine.get_all_stock_changes_since_last_stock_count()
        self.assertEqual(len(changes), 0)

    def test_temporary_count_line_no_stock_count(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 5,
                  'is_in': True},
                 {'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 7,
                  'is_in': True}
                 ]
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        changes, stock_count = TemporaryCounterLine.get_all_stock_changes_since_last_stock_count()
        self.assertEqual(len(changes), 2)

    def test_temporary_count_line_one_stock_count_no_new_lines(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 5,
                  'is_in': True},
                 {'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 7,
                  'is_in': True}
                 ]
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        StockCountDocument(user_modified=self.user_1).save()
        changes, stock_count = TemporaryCounterLine.get_all_stock_changes_since_last_stock_count()

        self.assertEqual(len(changes), 0)

    def test_temporary_count_line_one_stock_count_some_new_lines(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 5,
                  'is_in': True},
                 {'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 7,
                  'is_in': True}
                 ]
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        StockCountDocument(user_modified=self.user_1).save()
        entry = [{'article': self.articletype_2,
                  'book_value': self.cost_system_currency_2,
                  'count': 5,
                  'is_in': True},
                 ]
        # This prevents the next StockChange from being stores at the exact time as the StockCountDocument
        time.sleep(0.01)
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        changes, stock_count = TemporaryCounterLine.get_all_stock_changes_since_last_stock_count()
        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0].article, self.articletype_2)
        self.assertEqual(changes[0].count, 5)

    def test_temporary_counter_lines_no_previous_stock_counts(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 5,
                  'is_in': True},
                 {'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 7,
                  'is_in': True}
            , {'article': self.articletype_1,
               'book_value': self.cost_system_currency_1,
               'count': 3,
               'is_in': False},
                 {'article': self.articletype_2,
                  'book_value': self.cost_system_currency_2,
                  'count': 11,
                  'is_in': True},
                 {'article': self.articletype_2,
                  'book_value': self.cost_system_currency_2,
                  'count': 7,
                  'is_in': True},
                 {'article': self.articletype_2,
                  'book_value': self.cost_system_currency_2,
                  'count': 2,
                  'is_in': False}
                 ]
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
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
                  'book_value': self.cost_system_currency_1,
                  'count': IN_1,
                  'is_in': True},
                 {'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': IN_2,
                  'is_in': True},
                 {'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': OUT_1,
                  'is_in': False},
                 ]
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        sc = StockCountDocument(user_modified=self.user_1)
        sc.save()
        scl = StockCountLine(document=sc, article_type=self.articletype_1, previous_count=0, in_count=12,
                             out_count=3, physical_count=9, average_value=self.cost_system_currency_1, text="Foo",
                             accounting_group_id=1)
        scl.save()
        NEW_IN_1 = 1
        NEW_IN_2 = 2
        NEW_IN_TOTAL = NEW_IN_1 + NEW_IN_2
        NEW_OUT_1 = 4
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': NEW_IN_1,
                  'is_in': True},
                 {'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': NEW_IN_2,
                  'is_in': True},
                 {'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': NEW_OUT_1,
                  'is_in': False},
                 ]
        time.sleep(0.01)
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        changes, count = TemporaryCounterLine.get_all_stock_changes_since_last_stock_count()
        mods = TemporaryCounterLine.get_all_temporary_counterlines_since_last_stock_count(changes, count)
        correct = {
            self.articletype_1: TemporaryCounterLine(self.articletype_1, IN_TOTAL - OUT_1, NEW_IN_TOTAL, NEW_OUT_1),
            self.articletype_2: TemporaryCounterLine(self.articletype_2, 0, 0, 0)}
        for mod in mods:
            self.assertEqual(mod, correct.get(mod.article_type))

    def test_temporary_counter_lines_newly_used_article(self):
        IN_1 = 5
        IN_2 = 7
        IN_TOTAL = IN_1 + IN_2
        OUT_1 = 3
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': IN_1,
                  'is_in': True},
                 {'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': IN_2,
                  'is_in': True},
                 {'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': OUT_1,
                  'is_in': False},
                 ]
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        sc = StockCountDocument(user_modified=self.user_1)
        sc.save()
        scl = StockCountLine(document=sc, article_type=self.articletype_1, previous_count=0, in_count=12,
                             out_count=3, physical_count=9, average_value=self.cost_system_currency_1, text="Foo",
                             accounting_group_id=1)
        scl.save()
        NEW_IN_1 = 1
        NEW_IN_2 = 2
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': NEW_IN_1,
                  'is_in': True},
                 {'article': self.articletype_2,
                  'book_value': self.cost_system_currency_1,
                  'count': NEW_IN_2,
                  'is_in': True},
                 ]
        time.sleep(0.01)
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        changes, count = TemporaryCounterLine.get_all_stock_changes_since_last_stock_count()
        mods = TemporaryCounterLine.get_all_temporary_counterlines_since_last_stock_count(changes, count)
        correct = {self.articletype_1: TemporaryCounterLine(self.articletype_1, IN_TOTAL - OUT_1,
                                                            NEW_IN_1, 0, ),
                   self.articletype_2: TemporaryCounterLine(self.articletype_2, 0, NEW_IN_2, 0)}
        for mod in mods:
            self.assertEqual(mod, correct.get(mod.article_type))

    def test_keep_previous_count_no_stock_change(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 2,
                  'is_in': True},
                 ]
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        sc = StockCountDocument(user_modified=self.user_1)
        sc.save()
        scl = StockCountLine(document=sc, article_type=self.articletype_1, previous_count=0, in_count=2,
                             out_count=0, physical_count=2, average_value=self.cost_system_currency_1, text="Foo",
                             accounting_group_id=1)
        scl.save()
        entry = [{'article': self.articletype_2,
                  'book_value': self.cost_system_currency_1,
                  'count': 3,
                  'is_in': True},
                 ]
        time.sleep(0.01)
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        changes, count = TemporaryCounterLine.get_all_stock_changes_since_last_stock_count()
        mods = TemporaryCounterLine.get_all_temporary_counterlines_since_last_stock_count(changes, count)
        correct = {self.articletype_1: TemporaryCounterLine(self.articletype_1, 2, 0, 0),
                   self.articletype_2: TemporaryCounterLine(self.articletype_2, 0, 3, 0)}
        for mod in mods:
            self.assertEqual(mod, correct.get(mod.article_type))


class IntermediaryTests(TestCase, TestData):
    def setUp(self):
        # It is essential that the number of articleTypes does not diverge. Because of this, articleTypes
        # are saved in a fixed manner
        self.part_setup_vat_group()
        self.part_setup_currency()
        self.part_setup_accounting_group()
        self.part_setup_costs()
        self.part_setup_supplier()
        self.articletype_1 = ArticleType(name="ArticleType 1", accounting_group=self.accounting_group_components)
        self.articletype_1.save()
        self.articletype_2 = ArticleType(name="ArticleType 2", accounting_group=self.accounting_group_food)
        self.articletype_2.save()
        self.part_setup_users()

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

    def test_clear_temporary_counts(self):
        TemporaryArticleCount.clear_temporary_counts()
        tacs = TemporaryArticleCount.objects.all()
        self.assertEqual(len(tacs), 2)

    def test_partial_update_temporary_counts(self):
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 2)])
        TemporaryArticleCount.clear_temporary_counts()
        tacs = TemporaryArticleCount.objects.all()
        correct = {self.articletype_1: TemporaryArticleCount(article_type=self.articletype_1, count=0, checked=False),
                   self.articletype_2: TemporaryArticleCount(article_type=self.articletype_2, count=0, checked=False)}
        self.assertEqual(len(tacs), 2)
        for tac in tacs:
            self.assertEqual(tac, correct.get(tac.article_type))


class EndingTests(TestCase, TestData):
    def setUp(self):
        # It is essential that the number of articleTypes does not diverge. Because of this, articleTypes
        # are saved in a fixed manner
        self.part_setup_vat_group()
        self.part_setup_currency()
        self.part_setup_accounting_group()
        self.part_setup_costs()
        self.part_setup_supplier()
        self.articletype_1 = ArticleType(name="ArticleType 1", accounting_group=self.accounting_group_components)
        self.articletype_1.save()
        self.articletype_2 = ArticleType(name="ArticleType 2", accounting_group=self.accounting_group_food)
        self.articletype_2.save()
        self.part_setup_users()

    def test_get_discrepancies_not_enough_counts(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 2,
                  'is_in': True},
                 ]
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        with self.assertRaises(UncountedError):
            StockCountDocument.get_discrepancies()

    def test_get_discrepancies_not_checked(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 2,
                  'is_in': True},
                 ]
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        TemporaryArticleCount.clear_temporary_counts()
        with self.assertRaises(UncountedError):
            StockCountDocument.get_discrepancies()

    def test_get_discrepancies_no_discrepancies(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 2,
                  'is_in': True},
                 ]
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        TemporaryArticleCount.clear_temporary_counts()
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 2), (self.articletype_2, 0)])
        discs = StockCountDocument.get_discrepancies()
        self.assertEqual(len(discs), 0)

    def test_get_discrepancies_counted_but_should_be_zero(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 2,
                  'is_in': True},
                 ]
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        TemporaryArticleCount.clear_temporary_counts()
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 2), (self.articletype_2, 1)])
        discs = StockCountDocument.get_discrepancies()
        correct = (self.articletype_2, 1)
        self.assertEqual(len(discs), 1)
        self.assertEqual(discs[0], correct)

    def test_get_discrepancies_not_counted_but_should_be(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 2,
                  'is_in': True},
                 ]
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        TemporaryArticleCount.clear_temporary_counts()
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 0), (self.articletype_2, 0)])
        discs = StockCountDocument.get_discrepancies()
        correct = (self.articletype_1, -2)
        self.assertEqual(len(discs), 1)
        self.assertEqual(discs[0], correct)

    def test_get_discrepancies_two_discrepancies(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 2,
                  'is_in': True},
                 ]
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        TemporaryArticleCount.clear_temporary_counts()
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 1), (self.articletype_2, 1)])
        discs = StockCountDocument.get_discrepancies()
        correct = {self.articletype_1: (self.articletype_1, -1),
                   self.articletype_2: (self.articletype_2, 1)}
        self.assertEqual(len(discs), 2)
        for disc in discs:
            self.assertEqual(disc, correct.get(disc[0]))

    def test_get_discrepancies_previous_stock_count(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 2,
                  'is_in': True},
                 ]
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        sc = StockCountDocument(user_modified=self.user_1)
        sc.save()
        scl = StockCountLine(document=sc, article_type=self.articletype_1, previous_count=0, in_count=2,
                             out_count=0, physical_count=2, average_value=self.cost_system_currency_1, text="Foo",
                             accounting_group_id=1)
        scl.save()
        TemporaryArticleCount.clear_temporary_counts()
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 2), (self.articletype_2, 0)])
        discs = StockCountDocument.get_discrepancies()
        self.assertEqual(len(discs), 0)

    def test_get_discrepancies_different_previous_physical_count(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 2,
                  'is_in': True},
                 ]
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        sc = StockCountDocument(user_modified=self.user_1)
        sc.save()
        scl = StockCountLine(document=sc, article_type=self.articletype_1, previous_count=0, in_count=2,
                             out_count=0, physical_count=3, average_value=self.cost_system_currency_1, text="Foo",
                             accounting_group_id=1)
        scl.save()
        TemporaryArticleCount.clear_temporary_counts()
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 2), (self.articletype_2, 0)])
        discs = StockCountDocument.get_discrepancies()
        self.assertEqual(len(discs), 0)


class StockCountDocumentTests(TestCase, TestData):
    def setUp(self):
        # It is essential that the number of articleTypes does not diverge. Because of this, articleTypes
        # are saved in a fixed manner
        self.part_setup_vat_group()
        self.part_setup_currency()
        self.part_setup_accounting_group()
        self.part_setup_costs()
        self.part_setup_prices()
        self.part_setup_supplier()
        self.articletype_1 = ArticleType(name="ArticleType 1", accounting_group=self.accounting_group_components)
        self.articletype_1.save()
        self.articletype_2 = ArticleType(name="ArticleType 2", accounting_group=self.accounting_group_food)
        self.articletype_2.save()
        self.part_setup_users()
        self.part_setup_customers()

    def test_make_stock_count_no_discrepancies(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 2,
                  'is_in': True},
                 {'article': self.articletype_2,
                  'book_value': self.cost_system_currency_1,
                  'count': 3,
                  'is_in': True},
                 ]
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 2), (self.articletype_2, 3)])
        StockCountDocument.create_stock_count(self.user_1)
        doc = StockCountDocument.objects.get()
        correct = {self.articletype_1: StockCountLine(document=doc, article_type_id=self.articletype_1.id,
                                                      previous_count=0, in_count=2, out_count=0, physical_count=2,
                                                      average_value=self.cost_system_currency_1,
                                                      text=self.articletype_1.name,
                                                      accounting_group_id=self.articletype_1.accounting_group_id),
                   self.articletype_2: StockCountLine(document=doc, article_type_id=self.articletype_2.id, previous_count=0,
                                                      in_count=3, out_count=0, physical_count=3,
                                                      average_value=self.cost_system_currency_1,
                                                      text=self.articletype_2.name,
                                                      accounting_group_id=self.articletype_2.accounting_group_id)}
        scls = StockCountLine.objects.all()
        for scl in scls:
            self.assertEqual(scl, correct.get(scl.article_type))

    def test_add_two_stock_lines_no_differences(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 2,
                  'is_in': True},
                 {'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 3,
                  'is_in': True},
                 ]
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 5), (self.articletype_2, 0)])
        StockCountDocument.create_stock_count(self.user_1)
        doc = StockCountDocument.objects.get()
        zero_cost = Cost(amount=Decimal(0), use_system_currency=True)
        correct = {self.articletype_1: StockCountLine(document=doc, article_type_id=self.articletype_1.id, previous_count=0,
                                                      in_count=5, out_count=0, physical_count=5,
                                                      average_value=self.cost_system_currency_1,
                                                      text=self.articletype_1.name,
                                                      accounting_group_id=self.articletype_1.accounting_group_id),
                   self.articletype_2: StockCountLine(document=doc, article_type_id=self.articletype_2.id, previous_count=0,
                                                      in_count=0, out_count=0, physical_count=0,
                                                      average_value=zero_cost, text=self.articletype_2.name,
                                                      accounting_group_id=self.articletype_2.accounting_group_id)}
        scls = StockCountLine.objects.all()
        for scl in scls:
            self.assertEqual(scl, correct.get(scl.article_type))

    def test_add_two_stock_lines_different_labels(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 2,
                  'is_in': True},
                 {'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 3,
                  'is_in': True,
                  'label': OrderLabel(1)},
                 ]
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 5), (self.articletype_2, 0)])
        StockCountDocument.create_stock_count(self.user_1)
        doc = StockCountDocument.objects.get()
        zero_cost = Cost(amount=Decimal(0), use_system_currency=True)
        correct = {self.articletype_1: StockCountLine(document=doc, article_type_id=self.articletype_1.id, previous_count=0,
                                                      in_count=5, out_count=0, physical_count=5,
                                                      average_value=self.cost_system_currency_1,
                                                      text=self.articletype_1.name,
                                                      accounting_group_id=self.articletype_1.accounting_group_id),
                   self.articletype_2: StockCountLine(document=doc, article_type_id=self.articletype_2.id, previous_count=0,
                                                      in_count=0, out_count=0, physical_count=0,
                                                      average_value=zero_cost, text=self.articletype_2.name,
                                                      accounting_group_id=self.articletype_2.accounting_group_id)}
        scls = StockCountLine.objects.all()
        for scl in scls:
            self.assertEqual(scl, correct.get(scl.article_type))

    def test_more_counted_than_present(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 2,
                  'is_in': True},
                 {'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 3,
                  'is_in': True,
                  'label': OrderLabel(1)},
                 ]
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 6), (self.articletype_2, 0)])
        StockCountDocument.create_stock_count(self.user_1)
        doc = StockCountDocument.objects.get()
        zero_cost = Cost(amount=Decimal(0), use_system_currency=True)
        correct = {self.articletype_1: StockCountLine(document=doc, article_type_id=self.articletype_1.id, previous_count=0,
                                                      in_count=5, out_count=0, physical_count=6,
                                                      average_value=self.cost_system_currency_1,
                                                      text=self.articletype_1.name,
                                                      accounting_group_id=self.articletype_1.accounting_group_id),
                   self.articletype_2: StockCountLine(document=doc, article_type_id=self.articletype_2.id, previous_count=0,
                                                      in_count=0, out_count=0, physical_count=0,
                                                      average_value=zero_cost, text=self.articletype_2.name,
                                                      accounting_group_id=self.articletype_2.accounting_group_id)}
        scls = StockCountLine.objects.all()
        for scl in scls:
            self.assertEqual(scl, correct.get(scl.article_type))

        st = Stock.objects.get(article_id=self.articletype_1.id, labeltype__isnull=True)
        self.assertEqual(st.count, 3)

    def test_more_counted_nothing_present_on_line(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 3,
                  'is_in': True,
                  'label': OrderLabel(1)},
                 ]
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 5), (self.articletype_2, 0)])
        StockCountDocument.create_stock_count(self.user_1)
        doc = StockCountDocument.objects.get()
        zero_cost = Cost(amount=Decimal(0), use_system_currency=True)
        correct = {self.articletype_1: StockCountLine(document=doc, article_type_id=self.articletype_1.id, previous_count=0,
                                                      in_count=3, out_count=0, physical_count=5,
                                                      average_value=self.cost_system_currency_1,
                                                      text=self.articletype_1.name,
                                                      accounting_group_id=self.articletype_1.accounting_group_id),
                   self.articletype_2: StockCountLine(document=doc, article_type_id=self.articletype_2.id, previous_count=0,
                                                      in_count=0, out_count=0, physical_count=0,
                                                      average_value=zero_cost, text=self.articletype_2.name,
                                                      accounting_group_id=self.articletype_2.accounting_group_id)}
        scls = StockCountLine.objects.all()
        for scl in scls:
            self.assertEqual(scl, correct.get(scl.article_type))

        st = Stock.objects.get(article_id=self.articletype_1.id, labeltype__isnull=True)
        self.assertEqual(st.count, 2)

    def test_mixed_addition(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 3,
                  'is_in': True,
                  'label': OrderLabel(1)},
                 {'article': self.articletype_2,
                  'book_value': self.cost_system_currency_2,
                  'count': 1,
                  'is_in': True,
                  'label': OrderLabel(7)}
                 ]
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 7), (self.articletype_2, 4)])
        StockCountDocument.create_stock_count(self.user_1)
        doc = StockCountDocument.objects.get()
        correct = {self.articletype_1: StockCountLine(document=doc, article_type_id=self.articletype_1.id, previous_count=0,
                                                      in_count=3, out_count=0, physical_count=7,
                                                      average_value=self.cost_system_currency_1,
                                                      text=self.articletype_1.name,
                                                      accounting_group_id=self.articletype_1.accounting_group_id),
                   self.articletype_2: StockCountLine(document=doc, article_type_id=self.articletype_2.id, previous_count=0,
                                                      in_count=1, out_count=0, physical_count=4,
                                                      average_value=self.cost_system_currency_2,
                                                      text=self.articletype_2.name,
                                                      accounting_group_id=self.articletype_2.accounting_group_id)}
        scls = StockCountLine.objects.all()
        for scl in scls:
            self.assertEqual(scl, correct.get(scl.article_type))

        st_1 = Stock.objects.get(article_id=self.articletype_1.id, labeltype__isnull=True)
        self.assertEqual(st_1.count, 4)
        st_2 = Stock.objects.get(article_id=self.articletype_2.id, labeltype__isnull=True)
        self.assertEqual(st_2.count, 3)

    def test_addition_no_previous_stock(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 3,
                  'is_in': True},
                 ]
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 3), (self.articletype_2, 2)])
        StockCountDocument.create_stock_count(self.user_1)
        st_2 = Stock.objects.get(article_id=self.articletype_2.id, labeltype__isnull=True)
        self.assertEqual(st_2.count, 2)
        zero_cost = Cost(amount=Decimal(0), use_system_currency=True)
        self.assertEqual(st_2.book_value, zero_cost)

    def test_addition_cost_from_stock_change(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 3,
                  'is_in': True},
                 {'article': self.articletype_2,
                  'book_value': self.cost_system_currency_2,
                  'count': 3,
                  'is_in': True},
                 {'article': self.articletype_2,
                  'book_value': self.cost_system_currency_2,
                  'count': 3,
                  'is_in': False}
                 ]
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 3), (self.articletype_2, 2)])
        StockCountDocument.create_stock_count(self.user_1)
        st_2 = Stock.objects.get(article_id=self.articletype_2.id, labeltype__isnull=True)
        self.assertEqual(st_2.count, 2)
        self.assertEqual(st_2.book_value, self.cost_system_currency_2)

    def test_subtraction_no_solution(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 3,
                  'is_in': True},
                 ]
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 2), (self.articletype_2, 0)])
        with self.assertRaises(SolutionError):
            StockCountDocument.create_stock_count(self.user_1)

    def test_subtraction_wrong_solution(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 3,
                  'is_in': True},
                 ]
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 2), (self.articletype_2, 0)])
        DiscrepancySolution.add_solutions([DiscrepancySolution(article_type=self.articletype_1, stock_label="Order",
                                                               stock_key=1)])
        with self.assertRaises(SolutionError):
            StockCountDocument.create_stock_count(self.user_1)

    def test_subtraction_remove_from_stock(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 3,
                  'is_in': True},
                 ]
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 2), (self.articletype_2, 0)])
        DiscrepancySolution.add_solutions([DiscrepancySolution(article_type=self.articletype_1, stock_label=None,
                                                               stock_key=None)])
        StockCountDocument.create_stock_count(self.user_1)
        doc = StockCountDocument.objects.get()
        zero_cost = Cost(amount=Decimal(0), use_system_currency=True)
        correct = {self.articletype_1: StockCountLine(document=doc, article_type_id=self.articletype_1.id, previous_count=0,
                                                      in_count=3, out_count=0, physical_count=2,
                                                      average_value=self.cost_system_currency_1,
                                                      text=self.articletype_1.name,
                                                      accounting_group_id=self.articletype_1.accounting_group_id),
                   self.articletype_2: StockCountLine(document=doc, article_type_id=self.articletype_2.id, previous_count=0,
                                                      in_count=0, out_count=0, physical_count=0,
                                                      average_value=zero_cost, text=self.articletype_2.name,
                                                      accounting_group_id=self.articletype_2.accounting_group_id)}

        self.assertEqual(Stock.objects.get().count, 2)
        scls = StockCountLine.objects.all()
        for scl in scls:
            self.assertEqual(scl, correct[scl.article_type])

    def test_subtraction_from_labeled_line(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 3,
                  'is_in': True},
                 {'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 3,
                  'is_in': True,
                  'label': OrderLabel(1)}
                 ]
        ordr = Order(customer=self.customer_person_1)
        ordrlines = [OrderLine(order=ordr, state='A', wishable=self.articletype_1,
                               expected_sales_price=self.price_system_currency_1),
                     OrderLine(order=ordr, state='A', wishable=self.articletype_1,
                               expected_sales_price=self.price_system_currency_1),
                     OrderLine(order=ordr, state='A', wishable=self.articletype_1,
                               expected_sales_price=self.price_system_currency_1)]
        order_saved = Order.make_order(ordr, ordrlines, self.user_1)
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 4), (self.articletype_2, 0)])
        DiscrepancySolution.add_solutions([DiscrepancySolution(article_type=self.articletype_1, stock_label="Order",
                                                               stock_key=order_saved.id)])
        StockCountDocument.create_stock_count(self.user_1)
        st = Stock.objects.get(article_id=self.articletype_1.id, labelkey=order_saved.id)
        self.assertEqual(st.count, 1)
        lines = OrderLine.objects.filter(order=ordr)
        a_counted, c_counted = 0, 0
        for line in lines:
            if line.state == 'C':
                c_counted += 1
            elif line.state == 'A':
                a_counted += 1
        self.assertEqual(c_counted, 2)
        self.assertEqual(a_counted, 1)

    def test_subtraction_not_enough_solutions(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 3,
                  'is_in': True},
                 {'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 3,
                  'is_in': True,
                  'label': OrderLabel(1)}
                 ]
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 2), (self.articletype_2, 0)])
        DiscrepancySolution.add_solutions([DiscrepancySolution(article_type=self.articletype_1, stock_label="Order",
                                                               stock_key=1)])
        with self.assertRaises(SolutionError):
            StockCountDocument.create_stock_count(self.user_1)

    def test_correct_outs(self):
        entry = [{'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 2,
                  'is_in': True},
                 {'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 3,
                  'is_in': True,
                  'label': OrderLabel(1)},
                 {'article': self.articletype_1,
                  'book_value': self.cost_system_currency_1,
                  'count': 2,
                  'is_in': False,
                  'label': OrderLabel(1)}
                 ]
        StockChangeSet.construct(description="", entries=entry, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 3), (self.articletype_2, 0)])
        StockCountDocument.create_stock_count(self.user_1)
        doc = StockCountDocument.objects.get()
        zero_cost = Cost(amount=Decimal(0), use_system_currency=True)
        correct = {self.articletype_1: StockCountLine(document=doc, article_type_id=self.articletype_1.id, previous_count=0,
                                                      in_count=5, out_count=2, physical_count=3,
                                                      average_value=self.cost_system_currency_1,
                                                      text=self.articletype_1.name,
                                                      accounting_group_id=self.articletype_1.accounting_group_id),
                   self.articletype_2: StockCountLine(document=doc, article_type_id=self.articletype_2.id, previous_count=0,
                                                      in_count=0, out_count=0, physical_count=0,
                                                      average_value=zero_cost, text=self.articletype_2.name,
                                                      accounting_group_id=self.articletype_2.accounting_group_id)}
        scls = StockCountLine.objects.all()
        for scl in scls:
            self.assertEqual(scl, correct.get(scl.article_type))

    def test_non_zero_start_no_differences(self):
        entries = [{'article': self.articletype_1,
                    'book_value': self.cost_system_currency_1,
                    'count': 3,
                    'is_in': True},
                   {'article': self.articletype_2,
                    'book_value': self.cost_system_currency_2,
                    'count': 5,
                    'is_in': True}, ]
        StockChangeSet.construct(description="", entries=entries, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 3), (self.articletype_2, 5)])
        StockCountDocument.create_stock_count(self.user_1)
        entries = [{'article': self.articletype_1,
                    'book_value': self.cost_system_currency_1,
                    'count': 1,
                    'is_in': True},
                   {'article': self.articletype_2,
                    'book_value': self.cost_system_currency_2,
                    'count': 4,
                    'is_in': True}, ]
        time.sleep(0.1)
        StockChangeSet.construct(description="", entries=entries, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 4), (self.articletype_2, 9)])
        doc_2 = StockCountDocument.create_stock_count(self.user_1)
        count_lines = StockCountLine.objects.filter(document=doc_2)
        correct = {self.articletype_1: StockCountLine(document=doc_2, article_type_id=self.articletype_1.id, previous_count=3,
                                                      in_count=1, out_count=0, physical_count=4,
                                                      average_value=self.cost_system_currency_1,
                                                      text=self.articletype_1.name,
                                                      accounting_group_id=self.articletype_1.accounting_group_id),
                   self.articletype_2: StockCountLine(document=doc_2, article_type_id=self.articletype_2.id, previous_count=5,
                                                      in_count=4, out_count=0, physical_count=9,
                                                      average_value=self.cost_system_currency_2,
                                                      text=self.articletype_2.name,
                                                      accounting_group_id=self.articletype_2.accounting_group_id)}
        for line in count_lines:
            self.assertEqual(line, correct.get(line.article_type))

    def test_non_zero_start_positive_difference(self):
        entries = [{'article': self.articletype_1,
                    'book_value': self.cost_system_currency_1,
                    'count': 3,
                    'is_in': True},
                   {'article': self.articletype_2,
                    'book_value': self.cost_system_currency_2,
                    'count': 5,
                    'is_in': True}, ]
        StockChangeSet.construct(description="", entries=entries, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 4), (self.articletype_2, 5)])
        StockCountDocument.create_stock_count(self.user_1)
        entries = [{'article': self.articletype_1,
                    'book_value': self.cost_system_currency_1,
                    'count': 2,
                    'is_in': True},
                   {'article': self.articletype_2,
                    'book_value': self.cost_system_currency_2,
                    'count': 4,
                    'is_in': True}, ]
        time.sleep(0.1)
        StockChangeSet.construct(description="", entries=entries, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 6), (self.articletype_2, 9)])
        doc_2 = StockCountDocument.create_stock_count(self.user_1)
        count_lines = StockCountLine.objects.filter(document=doc_2)
        correct = {self.articletype_1: StockCountLine(document=doc_2, article_type_id=self.articletype_1.id, previous_count=3,
                                                      in_count=3, out_count=0, physical_count=6,
                                                      average_value=self.cost_system_currency_1,
                                                      text=self.articletype_1.name,
                                                      accounting_group_id=self.articletype_1.accounting_group_id),
                   self.articletype_2: StockCountLine(document=doc_2, article_type_id=self.articletype_2.id, previous_count=5,
                                                      in_count=4, out_count=0, physical_count=9,
                                                      average_value=self.cost_system_currency_2,
                                                      text=self.articletype_2.name,
                                                      accounting_group_id=self.articletype_2.accounting_group_id)}
        for line in count_lines:
            self.assertEqual(line, correct.get(line.article_type))

    def test_non_zero_two_consecutive_positive_differences(self):
        entries = [{'article': self.articletype_1,
                    'book_value': self.cost_system_currency_1,
                    'count': 3,
                    'is_in': True},
                   {'article': self.articletype_2,
                    'book_value': self.cost_system_currency_2,
                    'count': 5,
                    'is_in': True}, ]
        StockChangeSet.construct(description="", entries=entries, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 4), (self.articletype_2, 5)])
        StockCountDocument.create_stock_count(self.user_1)
        entries = [{'article': self.articletype_1,
                    'book_value': self.cost_system_currency_1,
                    'count': 2,
                    'is_in': True},
                   {'article': self.articletype_2,
                    'book_value': self.cost_system_currency_2,
                    'count': 4,
                    'is_in': True}, ]
        time.sleep(0.1)
        StockChangeSet.construct(description="", entries=entries, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 7), (self.articletype_2, 9)])
        doc_2 = StockCountDocument.create_stock_count(self.user_1)
        count_lines = StockCountLine.objects.filter(document=doc_2)
        correct = {self.articletype_1: StockCountLine(document=doc_2, article_type_id=self.articletype_1.id, previous_count=3,
                                                      in_count=3, out_count=0, physical_count=7,
                                                      average_value=self.cost_system_currency_1,
                                                      text=self.articletype_1.name,
                                                      accounting_group_id=self.articletype_1.accounting_group_id),
                   self.articletype_2: StockCountLine(document=doc_2, article_type_id=self.articletype_2.id, previous_count=5,
                                                      in_count=4, out_count=0, physical_count=9,
                                                      average_value=self.cost_system_currency_2,
                                                      text=self.articletype_2.name,
                                                      accounting_group_id=self.articletype_2.accounting_group_id)}
        for line in count_lines:
            self.assertEqual(line, correct.get(line.article_type))

    def test_non_zero_start_negative_difference(self):
        entries = [{'article': self.articletype_1,
                    'book_value': self.cost_system_currency_1,
                    'count': 3,
                    'is_in': True},
                   {'article': self.articletype_2,
                    'book_value': self.cost_system_currency_2,
                    'count': 5,
                    'is_in': True}, ]
        StockChangeSet.construct(description="", entries=entries, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 2), (self.articletype_2, 5)])
        DiscrepancySolution.add_solutions([DiscrepancySolution(article_type_id=self.articletype_1.id, stock_label=None, stock_key=None)])
        StockCountDocument.create_stock_count(self.user_1)
        entries = [{'article': self.articletype_1,
                    'book_value': self.cost_system_currency_1,
                    'count': 2,
                    'is_in': True},
                   {'article': self.articletype_2,
                    'book_value': self.cost_system_currency_2,
                    'count': 4,
                    'is_in': True}, ]
        time.sleep(0.1)
        StockChangeSet.construct(description="", entries=entries, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 4), (self.articletype_2, 9)])
        doc_2 = StockCountDocument.create_stock_count(self.user_1)
        count_lines = StockCountLine.objects.filter(document=doc_2)
        correct = {self.articletype_1: StockCountLine(document=doc_2, article_type_id=self.articletype_1.id, previous_count=3,
                                                      in_count=2, out_count=1, physical_count=4,
                                                      average_value=self.cost_system_currency_1,
                                                      text=self.articletype_1.name,
                                                      accounting_group_id=self.articletype_1.accounting_group_id),
                   self.articletype_2: StockCountLine(document=doc_2, article_type_id=self.articletype_2.id, previous_count=5,
                                                      in_count=4, out_count=0, physical_count=9,
                                                      average_value=self.cost_system_currency_2,
                                                      text=self.articletype_2.name,
                                                      accounting_group_id=self.articletype_2.accounting_group_id)}
        for line in count_lines:
            self.assertEqual(line, correct.get(line.article_type))

    def test_non_zero_two_consecutive_negative_differences(self):
        entries = [{'article': self.articletype_1,
                    'book_value': self.cost_system_currency_1,
                    'count': 3,
                    'is_in': True},
                   {'article': self.articletype_2,
                    'book_value': self.cost_system_currency_2,
                    'count': 5,
                    'is_in': True}, ]
        StockChangeSet.construct(description="", entries=entries, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 2), (self.articletype_2, 5)])
        DiscrepancySolution.add_solutions([DiscrepancySolution(article_type_id=self.articletype_1.id, stock_label=None, stock_key=None)])
        StockCountDocument.create_stock_count(self.user_1)
        entries = [{'article': self.articletype_1,
                    'book_value': self.cost_system_currency_1,
                    'count': 3,
                    'is_in': True},
                   {'article': self.articletype_1,
                    'book_value': self.cost_system_currency_1,
                    'count': 1,
                    'is_in': False},
                   {'article': self.articletype_2,
                    'book_value': self.cost_system_currency_2,
                    'count': 4,
                    'is_in': True}, ]
        time.sleep(0.1)
        StockChangeSet.construct(description="", entries=entries, source=StockChangeSet.SOURCE_TEST_DO_NOT_USE)
        TemporaryArticleCount.update_temporary_counts([(self.articletype_1, 4), (self.articletype_2, 9)])
        doc_2 = StockCountDocument.create_stock_count(self.user_1)
        count_lines = StockCountLine.objects.filter(document=doc_2)
        correct = {self.articletype_1: StockCountLine(document=doc_2, article_type_id=self.articletype_1.id, previous_count=3,
                                                      in_count=3, out_count=2, physical_count=4,
                                                      average_value=self.cost_system_currency_1,
                                                      text=self.articletype_1.name,
                                                      accounting_group_id=self.articletype_1.accounting_group_id),
                   self.articletype_2: StockCountLine(document=doc_2, article_type_id=self.articletype_2.id, previous_count=5,
                                                      in_count=4, out_count=0, physical_count=9,
                                                      average_value=self.cost_system_currency_2,
                                                      text=self.articletype_2.name,
                                                      accounting_group_id=self.articletype_2.accounting_group_id)}
        for line in count_lines:
            self.assertEqual(line, correct.get(line.article_type))

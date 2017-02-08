import datetime
from decimal import Decimal

from django.test import TestCase

from money.models import Cost
from supplier.models import SupplierTypeArticle, SupplierTypeArticleProcessingError, ArticleTypeSupplier, ArticleType
from tools.testing import TestData


class SupplierTypeArticleUpdaterTests(TestCase, TestData):
    def setUp(self):
        self.setup_base_data()

    def test_insertion_of_new_lines_without_old_lines(self):
        sta1 = SupplierTypeArticle(supplier=self.supplier_1, cost=self.cost_system_currency_1, number="ABC",
                                   name="Some description", minimum_number_to_order=1)
        sta2 = SupplierTypeArticle(supplier=self.supplier_1, cost=self.cost_system_currency_2, number="ABC2",
                                   name="Some description!", minimum_number_to_order=2)
        stas = [sta1, sta2]  # type: list[SupplierTypeArticle]
        SupplierTypeArticle.process_supplier_type_articles(stas)
        stored_stas = SupplierTypeArticle.objects.all()
        correct = {"ABC": SupplierTypeArticle(supplier=self.supplier_1, cost=self.cost_system_currency_1, number="ABC",
                                              name="Some description", minimum_number_to_order=1),
                   "ABC2": SupplierTypeArticle(supplier=self.supplier_1, cost=self.cost_system_currency_2,
                                               number="ABC2",
                                               name="Some description!", minimum_number_to_order=2)}
        for st in stored_stas:
            self.assertEqual(st, correct[st.number])

    def test_insertion_does_update(self):
        # Some base data to save
        sta1 = SupplierTypeArticle(supplier=self.supplier_1, cost=self.cost_system_currency_1, number="ABC",
                                   name="Some description", minimum_number_to_order=1)
        sta2 = SupplierTypeArticle(supplier=self.supplier_1, cost=self.cost_system_currency_2, number="ABC2",
                                   name="Some description!", minimum_number_to_order=2)
        sta1.save()
        sta2.save()
        sta1_new = SupplierTypeArticle(supplier=self.supplier_1, cost=self.cost_system_currency_1, number="ABC",
                                       name="Updated description", minimum_number_to_order=1)
        cost_new = Cost(amount=self.cost_system_currency_1.amount * Decimal(1.1), use_system_currency=True)
        sta_2_new = SupplierTypeArticle(supplier=self.supplier_1, cost=cost_new, number="ABC2",
                                        name="Some description!", minimum_number_to_order=2)
        stas = [sta1_new, sta_2_new]
        SupplierTypeArticle.process_supplier_type_articles(stas)
        new_stas = SupplierTypeArticle.objects.all()
        self.assertEqual(2, len(new_stas))
        for sta in new_stas:
            if sta.number == "ABC":
                self.assertEqual(sta.name, "Updated description")
            elif sta.number == 'ABC2':
                self.assertEqual(sta.cost, cost_new)

    def test_update_multiple_attributes(self):
        sta1 = SupplierTypeArticle(supplier=self.supplier_1, cost=self.cost_system_currency_1, number="ABC",
                                   name="Some description", minimum_number_to_order=1)
        sta1.save()
        sta1_new = SupplierTypeArticle(supplier=self.supplier_1, cost=self.cost_system_currency_1, number="ABC",
                                       name="Some description!!", minimum_number_to_order=2)
        SupplierTypeArticle.process_supplier_type_articles([sta1_new])
        sta_gotten = SupplierTypeArticle.objects.get()
        self.assertEqual(sta_gotten, sta1_new)

    def test_mixing_suppliers_does_not_work(self):
        sta1 = SupplierTypeArticle(supplier=self.supplier_1)
        sta2 = SupplierTypeArticle(supplier=self.supplier_2)
        stas = [sta1, sta2]
        with self.assertRaises(SupplierTypeArticleProcessingError):
            SupplierTypeArticle.process_supplier_type_articles(stas)

    def test_too_high_cost_ratio(self):
        sta1 = SupplierTypeArticle(supplier=self.supplier_1, cost=self.cost_system_currency_1, number="ABC",
                                   name="Some description", minimum_number_to_order=1)
        sta1.save()
        cost_new = Cost(
            amount=self.cost_system_currency_1.amount * Decimal((SupplierTypeArticle.VALID_COST_RATIO_BOUND + 0.1)),
            currency=self.cost_system_currency_1.currency)
        sta1_new = SupplierTypeArticle(supplier=self.supplier_1, cost=cost_new, number="ABC",
                                       name="Some description", minimum_number_to_order=2)
        SupplierTypeArticle.process_supplier_type_articles([sta1_new])
        sta_gotten = SupplierTypeArticle.objects.get()
        self.assertEqual(sta_gotten, sta1)

    def test_too_low_cost_ratio(self):
        sta1 = SupplierTypeArticle(supplier=self.supplier_1, cost=self.cost_system_currency_1, number="ABC",
                                   name="Some description", minimum_number_to_order=1)
        sta1.save()
        cost_new = Cost(
            amount=self.cost_system_currency_1.amount / Decimal((SupplierTypeArticle.VALID_COST_RATIO_BOUND + 0.1)),
            currency=self.cost_system_currency_1.currency)
        sta1_new = SupplierTypeArticle(supplier=self.supplier_1, cost=cost_new, number="ABC",
                                       name="Some description", minimum_number_to_order=2)
        SupplierTypeArticle.process_supplier_type_articles([sta1_new])
        sta_gotten = SupplierTypeArticle.objects.get()
        self.assertEqual(sta_gotten, sta1)

    def test_too_high_minimum_order_amount_ratio(self):
        sta1 = SupplierTypeArticle(supplier=self.supplier_1, cost=self.cost_system_currency_1, number="ABC",
                                   name="Some description", minimum_number_to_order=1)
        sta1.save()
        cost_new = Cost(
            amount=self.cost_system_currency_1.amount * Decimal((SupplierTypeArticle.VALID_COST_RATIO_BOUND + 0.1)),
            use_system_currency=True)
        sta1_new = SupplierTypeArticle(supplier=self.supplier_1, cost=cost_new, number="ABC",
                                       name="Some description", minimum_number_to_order=2)
        SupplierTypeArticle.process_supplier_type_articles([sta1_new])
        sta_gotten = SupplierTypeArticle.objects.get()
        self.assertEqual(sta_gotten, sta1)

    def test_too_low_minimum_order_amount_ratio(self):
        sta1 = SupplierTypeArticle(supplier=self.supplier_1, cost=self.cost_system_currency_1, number="ABC",
                                   name="Some description", minimum_number_to_order=4)
        sta1.save()
        cost_new = Cost(
            amount=self.cost_system_currency_1.amount * Decimal((SupplierTypeArticle.VALID_COST_RATIO_BOUND + 0.1))
            , use_system_currency=True)
        sta1_new = SupplierTypeArticle(supplier=self.supplier_1, cost=cost_new, number="ABC",
                                       name="Some description", minimum_number_to_order=1)
        SupplierTypeArticle.process_supplier_type_articles([sta1_new])
        sta_gotten = SupplierTypeArticle.objects.get()
        self.assertEqual(sta_gotten, sta1)

    def test_no_interference_from_different_articles(self):
        sta1 = SupplierTypeArticle(supplier=self.supplier_1, cost=self.cost_system_currency_1, number="ABC",
                                   name="Some description", minimum_number_to_order=1)
        sta1.save()
        sta_2_new = SupplierTypeArticle(supplier=self.supplier_1, cost=self.cost_system_currency_1, number="ABC2",
                                        name="Some description!", minimum_number_to_order=2)
        stas = [sta_2_new]
        SupplierTypeArticle.process_supplier_type_articles(stas)
        new_stas = SupplierTypeArticle.objects.all()
        self.assertEqual(len(new_stas), 2)
        correct = {"ABC": sta1,
                   "ABC2": sta_2_new}
        for sta in new_stas:
            self.assertEqual(sta, correct[sta.number])

    def test_old_articles_deleted_without_match(self):
        too_old_date = datetime.date.today() - datetime.timedelta(days=(SupplierTypeArticle.CLEAN_UP_LIMIT + 2))
        sta1 = SupplierTypeArticle(supplier=self.supplier_1, cost=self.cost_system_currency_1, number="ABC",
                                   name="Some description", minimum_number_to_order=1, date_updated=too_old_date)
        sta1.save()
        sta_2_new = SupplierTypeArticle(supplier=self.supplier_1, cost=self.cost_system_currency_1, number="ABC2",
                                        name="Some description!", minimum_number_to_order=2)
        stas = [sta_2_new]
        SupplierTypeArticle.process_supplier_type_articles(stas)
        self.assertEqual(SupplierTypeArticle.objects.get(), sta_2_new)

    def test_delete_too_old_articles_even_if_details_change_too_much(self):
        too_old_date = datetime.date.today() - datetime.timedelta(days=(SupplierTypeArticle.CLEAN_UP_LIMIT + 2))
        sta1 = SupplierTypeArticle(supplier=self.supplier_1, cost=self.cost_system_currency_1, number="ABC",
                                   name="Some description", minimum_number_to_order=1, date_updated=too_old_date)
        sta1.save()
        sta_1_new = SupplierTypeArticle(supplier=self.supplier_1, cost=self.cost_system_currency_1, number="ABC",
                                        name="Some description!", minimum_number_to_order=4)
        stas = [sta_1_new]
        SupplierTypeArticle.process_supplier_type_articles(stas)
        self.assertEqual(SupplierTypeArticle.objects.get(), sta_1_new)


# noinspection PyUnusedLocal
class ArticleTypeSupplierTests(TestCase, TestData):
    def setUp(self):
        self.part_setup_currency_data()
        self.part_setup_vat_group()
        self.part_setup_currency()
        self.part_setup_accounting_group()
        self.part_setup_payment_types()
        self.part_setup_registers()
        self.part_setup_denominations()
        self.part_setup_prices()
        self.part_setup_costs()
        self.part_setup_supplier()
        self.part_setup_article_types()
        self.articletypesupplier_article_1 = ArticleTypeSupplier(supplier=self.supplier_1,
                                                                 article_type=self.articletype_1,
                                                                 cost=self.cost_system_currency_1, availability='A',
                                                                 supplier_string="SupplierArticleType 1",
                                                                 minimum_number_to_order=1)
        self.articletypesupplier_article_1.save()
        self.articletypesupplier_article_2 = ArticleTypeSupplier(supplier=self.supplier_1,
                                                                 article_type=self.articletype_2,
                                                                 cost=self.cost_system_currency_2, availability='A',
                                                                 supplier_string="SupplierArticleType 2",
                                                                 minimum_number_to_order=1)
        self.articletypesupplier_article_2.save()

    def test_update_ats_simple(self):
        ats_1 = self.articletypesupplier_article_1
        sta_1 = SupplierTypeArticle(supplier=self.supplier_1,
                                    cost=self.cost_system_currency_1, number="SupplierArticleType 1",
                                    name="Meh", minimum_number_to_order=2, supply=1)
        sta_1.save()
        ArticleTypeSupplier.update_article_type_suppliers(self.supplier_1)
        at_updated = ArticleTypeSupplier.objects.get(article_type=self.articletype_1)
        self.assertEqual(at_updated.minimum_number_to_order, 2)
        self.assertEqual(at_updated.availability, 'A')
        sta_updated = SupplierTypeArticle.objects.get()
        self.assertEqual(sta_updated.article_type_supplier, at_updated)

    def test_no_supply_means_state_change(self):
        sta_1 = SupplierTypeArticle(supplier=self.supplier_1,
                                    cost=self.cost_system_currency_1, number="SupplierArticleType 1",
                                    name="Meh", minimum_number_to_order=2, supply=0)
        sta_1.save()
        ArticleTypeSupplier.update_article_type_suppliers(self.supplier_1)
        at_updated = ArticleTypeSupplier.objects.get(article_type=self.articletype_1)
        self.assertEqual(at_updated.availability, 'L')

    def test_no_stas_means_no_supply_and_update(self):
        ArticleTypeSupplier.update_article_type_suppliers(self.supplier_1)
        at_updated = ArticleTypeSupplier.objects.get(article_type=self.articletype_1)
        self.assertEqual(at_updated.availability, 'D')

    def test_extra_sta_has_no_effect(self):
        self.articletype_3 = ArticleType(name="ArticleType 2", accounting_group=self.accounting_group_food)
        ArticleTypeSupplier.update_article_type_suppliers(self.supplier_1)
        self.assertEqual(ArticleTypeSupplier.objects.count(), 2)

    def test_readding_supply_resets_ats_state(self):
        self.articletypesupplier_article_1.availability = 'D'
        self.articletypesupplier_article_1.save()
        sta_1 = SupplierTypeArticle(supplier=self.supplier_1,
                                    cost=self.cost_system_currency_1, number="SupplierArticleType 1",
                                    name="Meh", minimum_number_to_order=2, supply=1)
        sta_1.save()
        ArticleTypeSupplier.update_article_type_suppliers(self.supplier_1)
        at_updated = ArticleTypeSupplier.objects.get(article_type=self.articletype_1)
        self.assertEqual(at_updated.availability, 'A')

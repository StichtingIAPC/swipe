from django.test import TestCase
from article.models import *
from money.models import VAT
from django.db import connection


class INeedSettings:
    def setUp(self):
        self.vat_group = VAT()
        self.vat_group.name="Bar"
        self.vat_group.active=True
        self.vat_group.vatrate=1.12
        self.vat_group.save()
        self.acc_group = AccountingGroup()
        self.acc_group.accounting_number = 2
        self.acc_group.vat_group = self.vat_group
        self.acc_group.save()

        self.branch = AssortmentArticleBranch.objects.create(
            name='hoi',
            parent_tag=None)

        self._base_article_settings = {
            'accounting_group': self.acc_group,
            'name': 'test',
            'branch': self.branch
        }


class ArticleBasicTests(INeedSettings, TestCase):
    def setUp(self):
        super().setUp()
        self.vat_group = VAT()
        self.vat_group.name="Bar"
        self.vat_group.active=True
        self.vat_group.vatrate=1.12
        self.vat_group.save()
        self.acc_group = AccountingGroup()
        self.acc_group.accounting_number = 2
        self.acc_group.vat_group = self.vat_group
        self.acc_group.save()

    def test_illegal_save(self):
        generic_wishable_type = WishableType()
        generic_wishable_type.name = "foo"
        self.assertRaises(AbstractClassInitializationError, generic_wishable_type.save)
        generic_wishable_type = SellableType()
        generic_wishable_type.name = "foo"
        self.assertRaises(AbstractClassInitializationError, generic_wishable_type.save)

    def test_legal_save(self):
        article_type = ArticleType(branch=self.branch)
        article_type.name = "Foo"
        article_type.accounting_group = self.acc_group
        blocked = False
        try:
            article_type.save()
        except AbstractClassInitializationError:
            blocked = True
        assert not blocked

        and_product_type = AndProductType(**self._base_article_settings)
        blocked = False
        try:
            and_product_type.save()
        except AbstractClassInitializationError:
            blocked = True
        assert not blocked

    def test_inheritance(self):
            article_type = ArticleType(branch=self.branch)
            article_type.name = "Foo"
            article_type.accounting_group = self.acc_group
            article_type.save()
            assert (article_type.name == "Foo")
            results = WishableType.objects.select_related().all()
            for result in results:
                assert result.sellabletype.articletype.name == "Foo"
                if hasattr(result,"sellabletype"):
                    if hasattr(result.sellabletype,"articletype"):
                        assert(result.sellabletype.articletype.accounting_group.accounting_number == 2)
                else:
                    raise Exception("Typing error: Abstract class is given while implementing type expected")

    def test_subclassing(self):
            andproduct_type = AndProductType(branch=self.branch)
            andproduct_type.name="Test"
            andproduct_type.save()
            orproduct_type = OrProductType(branch=self.branch)
            orproduct_type.name="Bar"
            orproduct_type.save()
            article_type = ArticleType(branch=self.branch)
            article_type.name = "Foo"
            article_type.accounting_group = self.acc_group
            article_type.save()
            results = WishableType.objects.select_related('sellabletype','orproducttype','sellabletype__articletype').all()
            assert (results.count() == 3)
            results2 = AndProductType.objects.all()
            assert results2.count() == 1
            results3 = OrProductType.objects.all()
            assert results3.count() == 1
            results4 = ArticleType.objects.all()
            assert results4.count() == 1



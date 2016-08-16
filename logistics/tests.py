from django.test import TestCase
from money.models import VAT, Price, Currency, AccountingGroup, Money
from article.models import ArticleType
from crm.models import User, Person
from logistics.models import *
from decimal import Decimal


class StockWishTests(TestCase):

    def setUp(self):
        self.vat_group = VAT()
        self.vat_group.name = "AccGrpFoo"
        self.vat_group.active = True
        self.vat_group.vatrate = 1.12
        self.vat_group.save()
        self.price = Price(amount=Decimal("1.00"), use_system_currency=True)
        self.currency = Currency(iso="USD")

        self.acc_group = AccountingGroup()
        self.acc_group.accounting_number = 2
        self.acc_group.vat_group = self.vat_group
        self.acc_group.save()

        self.article_type = ArticleType(accounting_group=self.acc_group, name="Foo1")
        self.article_type.save()

        self.at2 = ArticleType(accounting_group=self.acc_group, name="Foo2")
        self.at2.save()

        self.at3 = ArticleType(accounting_group=self.acc_group, name="Foo3")
        self.at3.save()

        self.money = Money(amount=Decimal(3.32), currency=self.currency)

        self.customer = Person()
        self.customer.save()

        self.copro = User()
        self.copro.save()

    def test_primitive_wish_save(self):

        sw = StockWish(copro=self.copro)
        sw.save()
        NUMBER = 2

        swl1 = StockWishLine(article_type=self.article_type, number=NUMBER, stock_wish=sw)
        swl1.save()

        assert len(StockWish.objects.all()) == 1
        assert len(StockWishLine.objects.all()) == 1
        swl = StockWishLine.objects.get()
        assert swl.stock_wish == sw

        swtl = StockWishTableLine.objects.all()
        assert len(swtl) == 1
        assert swtl[0].article_type == self.article_type
        assert swtl[0].number == NUMBER

    def test_addition_wish(self):

        sw = StockWish(copro=self.copro)
        sw.save()
        NUMBER = 2

        swl1 = StockWishLine(article_type=self.article_type, number=NUMBER, stock_wish=sw)
        swl1.save()

        NUMBER2 = 3
        swl2 = StockWishLine(article_type=self.article_type, number=NUMBER2, stock_wish=sw)
        swl2.save()
        swtl = StockWishTableLine.objects.all()
        assert len(swtl) == 1
        assert swtl[0].number == NUMBER + NUMBER2

        logs = StockWishTableLog.objects.all()
        assert len(logs) == 2

        assert logs[0].supplier_order is None and logs[0].stock_wish == sw

    def test_differentiation_wish(self):
        sw = StockWish(copro=self.copro)
        sw.save()
        NUMBER = 2

        swl1 = StockWishLine(article_type=self.article_type, number=NUMBER, stock_wish=sw)
        swl1.save()

        NUMBER2 = 3
        swl2 = StockWishLine(article_type=self.at2, number=NUMBER2, stock_wish=sw)
        swl2.save()

        swtls = StockWishTableLine.objects.all()
        assert len(swtls) == 2

        for swtl in swtls:
            if swtl.article_type == self.article_type:
                assert swtl.number == NUMBER
            else:
                assert swtl.number == NUMBER2

        assert len(StockWishTableLog.objects.all()) == 2

    def test_mass_storage_simple(self):

        atcs = []
        atcs.append([self.article_type, 2])
        StockWish.create_stock_wish(self.copro, atcs)

        stockwish_list = StockWish.objects.all()
        assert len(stockwish_list) == 1
        assert stockwish_list[0].copro == self.copro

        logs = StockWishTableLog.objects.all()
        assert len(logs) == 1

        swl = StockWishLine.objects.all()
        assert len(swl) == 1
        assert swl[0].stock_wish == stockwish_list[0]

    def test_mass_storage_compound(self):

        atcs = []
        atcs.append([self.article_type, 2])
        atcs.append([self.article_type, 2])
        StockWish.create_stock_wish(self.copro, atcs)

        stockwish_list = StockWish.objects.all()
        assert len(stockwish_list) == 1
        assert stockwish_list[0].copro == self.copro

        logs = StockWishTableLog.objects.all()
        assert len(logs) == 2

        swl = StockWishLine.objects.all()
        assert len(swl) == 2
        assert swl[0].stock_wish == stockwish_list[0]
        assert swl[1].stock_wish == stockwish_list[0]

        stock_wish_table_lines = StockWishTableLine.objects.all()
        assert len(stock_wish_table_lines) == 1

    def test_mass_storage_differentiated(self):

        atcs = []
        atcs.append([self.article_type, 2])
        atcs.append([self.article_type, 2])
        atcs.append([self.at2, 3])
        atcs.append([self.at3, 5])
        StockWish.create_stock_wish(self.copro, atcs)

        stockwish_list = StockWish.objects.all()
        assert len(stockwish_list) == 1
        assert stockwish_list[0].copro == self.copro

        logs = StockWishTableLog.objects.all()
        assert len(logs) == 4

        swl = StockWishLine.objects.all()
        assert len(swl) == 4
        stock_wish_table_lines = StockWishTableLine.objects.all()
        assert len(stock_wish_table_lines) == 3

    def test_indirection(self):

        log = StockWishTableLog(number=3, article_type=self.article_type)
        caught = False
        try:
            log.save()
        except IndirectionError:
            caught = True
        assert caught




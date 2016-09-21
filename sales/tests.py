from django.test import TestCase
from article.tests import INeedSettings
from money.models import Currency, Cost, Money, VAT, Price, AccountingGroup
from register.models import SalesPeriod, InactiveError
from decimal import Decimal
from article.models import ArticleType
from sales.models import SalesTransactionLine, Payment, Transaction, NotEnoughStockError
from stock.models import StockChange, StockSmallerThanZeroError, StockChangeSet
from register.models import PaymentType
from crm.models import User
from tools.util import _assert


class TestTransactionCreationFunction(INeedSettings, TestCase):

    def setUp(self):
        super().setUp()
        self.EUR = Currency("EUR")
        self.cost = Cost(Decimal("1.21000"), self.EUR)
        self.money = Money(Decimal("1.21000"), self.EUR)
        self.pt = PaymentType.objects.create()
        self.vat = VAT.objects.create(vatrate=Decimal("1.21"), name="HIGH", active=True)
        self.price = Price(Decimal("1.21000"), vat=self.vat.vatrate, currency=self.EUR)
        self.acc_group = AccountingGroup.objects.create(vat_group=self.vat, accounting_number=1, name='hoihoi')
        self.art = ArticleType.objects.create(name="P1", branch=self.branch,
                                              accounting_group=self.acc_group)
        self.sp = SalesPeriod.objects.create()
        self.simplest = SalesTransactionLine(article=self.art, count=1, cost=self.cost, price=self.price, num=1)
        self.simple_payment = Payment(amount=self.money, payment_type=self.pt)
        self.copro = User()
        self.copro.save()


    def test_not_enough_stock_error(self):
        oalist = []
        oalist.append(SalesTransactionLine(price=self.price, count=1, order=None, article=self.art))
        caught = False
        try:
            Transaction.create_transaction(user=self.copro, payments=[self.simple_payment], transaction_lines=oalist)
        except NotEnoughStockError:
            caught = True
        _assert(caught)

    def test_dict_manual(self):
        dt = {}
        dt[(2, self.art)] = 2

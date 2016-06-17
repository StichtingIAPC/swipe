from django.test import TestCase
from article.models import *
from money.models import *
from order.models import *
# Create your tests here.



class OrderTest(TestCase):

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

        self.article_type = ArticleType(accounting_group=self.acc_group,name="Foo")
        self.article_type.save()

        self.customer = Person()
        self.customer.save()

        self.copro = User()
        self.copro.save()

    def test_save_speed(self):
        b=[None]*1001
        b[1000]
        big_order=Order(copro=self.copro, customer=self.customer)
        big_order.save()
        orderlines = []
        for i in range (0, 100):
            orderLine = OrderLine(order=big_order, wishable=self.article_type)
            orderlines.append(orderLine)

        for ol in orderlines:
            ol.save()

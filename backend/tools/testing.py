import datetime
from decimal import Decimal

from django.test import TestCase

from article.models import ArticleType, OtherCostType
from crm.models import User, Person, Customer, Organisation, ContactOrganisation
from externalise.models import ExternaliseDocument
from logistics.models import SupplierOrder, StockWish
from money.models import VAT, Currency, AccountingGroup, Denomination, Cost, Price, CurrencyData, Money, VATPeriod, \
    SalesPrice
from order.models import Order
from pricing.models import PricingModel
from register.models import PaymentType, Register
from sales.models import Transaction, SalesTransactionLine, Payment, OtherCostTransactionLine
from supplication.models import PackingDocument
from supplier.models import Supplier, ArticleTypeSupplier
from swipe.settings import USED_CURRENCY


def allowFailure(arg):
    exception = arg if issubclass(arg, BaseException) else BaseException

    def wrapper(wrapped):
        def result(*args, **kwargs):
            try:
                return wrapped(*args, **kwargs)
            except exception as e:
                return
        return result

    if issubclass(arg, BaseException):
        return wrapper
    else:
        return wrapper(arg)


# noinspection PyAttributeOutsideInit
class TestData:
    """
    Test data for usage in unit and integrations tests. For most use cases it is enough to let a testclass extend
    TestData and then call 'setup_base_data()' on self. For fine grained testing, use the part setup functions and the
    dd setup functions to inject just that bit of data you need. Things like customer and supplier orders can also be
    done with these functions to generate some 'real' data for usage. Can also be used in manual testing situations.
    """

    def setup_base_data(self):
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
        self.part_setup_article_type_supplier()
        self.part_setup_othercosts()
        self.part_setup_customers()
        self.part_setup_users()

    def part_setup_currency_data(self):
        self.currency_data_eur, none = CurrencyData.objects.get_or_create(iso="EUR", name="Euro", symbol="€", digits=2)
        self.currency_data_usd, none = CurrencyData.objects.get_or_create(iso="USD", name="US Dollar", symbol="$", digits=2)
        if USED_CURRENCY == "EUR":
            self.currency_data_used = self.currency_data_eur
        elif USED_CURRENCY == "USD":
            self.currency_data_used = self.currency_data_usd
        else:
            self.currency_data_used = CurrencyData(iso=USED_CURRENCY, name="Default Currency", symbol="?", digits=2)
            self.currency_data_used.save()

    def part_setup_vat_group(self):
        self.vat_group_high, none = VAT.objects.get_or_create(name="High", active=True)
        self.vat_group_low, none = VAT.objects.get_or_create(name="Low", active=True)
        self.vat_group_high_period = VATPeriod.objects.get_or_create(vat=self.vat_group_high, begin_date=datetime.date.fromtimestamp(1000000),
                                                                     vatrate=Decimal(1.21))
        self.vat_group_low_period = VATPeriod.objects.get_or_create(vat=self.vat_group_low, begin_date=datetime.date.fromtimestamp(1000000),
                                                                    vatrate=Decimal(1.06))

    def part_setup_currency(self):
        self.currency_eur = Currency(iso="EUR")
        self.currency_usd = Currency(iso="USD")
        self.currency_current = Currency(iso=USED_CURRENCY)

    def part_setup_accounting_group(self):
        self.accounting_group_components, none = AccountingGroup.objects.get_or_create(name="Components", vat_group=self.vat_group_high,
                                                           accounting_number=1)
        self.accounting_group_food, none = AccountingGroup.objects.get_or_create(name="Food", vat_group=self.vat_group_low, accounting_number=2)

    def part_setup_payment_types(self):
        self.paymenttype_cash, none = PaymentType.objects.get_or_create(name="Cash")
        self.paymenttype_maestro, none = PaymentType.objects.get_or_create(name="Maestro")
        self.paymenttype_invoice, none = PaymentType.objects.get_or_create(name="Invoice", is_invoicing=True)

    def part_setup_registers(self):
        self.register_1, none = Register.objects.get_or_create(currency=self.currency_data_eur, is_cash_register=True,
                                   payment_type=self.paymenttype_cash, name="Register 1")
        self.register_2, none = Register.objects.get_or_create(currency=self.currency_data_eur, is_cash_register=True,
                                   payment_type=self.paymenttype_cash, name="Register 2")
        self.register_3, none = Register.objects.get_or_create(currency=self.currency_data_used, is_cash_register=False,
                                   payment_type=self.paymenttype_maestro, name="Register 3")
        self.register_4, none = Register.objects.get_or_create(currency=self.currency_data_used, is_cash_register=False,
                                   payment_type=self.paymenttype_invoice, name="Register 4")

    def part_setup_denominations(self):
        self.denomination_eur_20, none = Denomination.objects.get_or_create(currency=self.currency_data_eur, amount=20)
        self.denomination_eur_0_01, none = Denomination.objects.get_or_create(currency=self.currency_data_eur, amount=0.01)

    def part_setup_prices(self):
        self.price_system_currency_1 = SalesPrice(amount=Decimal("1.72674"), currency=Currency("EUR"), vat=Decimal("1.21000"), cost=Cost(currency=Currency("EUR"),amount=Decimal("1.23000")))
        self.price_systen_currency_2 = SalesPrice(amount=Decimal("2.54384"), currency=Currency("EUR"), vat=Decimal("1.06000"), cost=Cost(currency=Currency("EUR"),amount=Decimal("2.10000")))

    def part_setup_costs(self):
        self.cost_system_currency_1 = Cost(amount=Decimal(1.23), use_system_currency=True)
        self.cost_system_currency_2 = Cost(amount=Decimal(2.10), use_system_currency=True)
        self.cost_system_currency_3 = Cost(amount=Decimal(3.14), use_system_currency=True)
        self.cost_system_currency_4 = Cost(amount=Decimal(10.01), use_system_currency=True)

    def part_setup_supplier(self):
        self.supplier_1, none = Supplier.objects.get_or_create(name="Supplier 1")
        self.supplier_2, none = Supplier.objects.get_or_create(name="Supplier 2")

    def part_setup_article_types(self):
        ats = ArticleType.objects.all()
        if len(ats) >=2:
            self.articletype_1 = ats[0]
            self.articletype_2 = ats[1]
        else:
            self.articletype_1 = ArticleType.objects.create(name="ArticleType 1",
                                                                         accounting_group=self.accounting_group_components, serial_number=False)
            self.articletype_2 = ArticleType.objects.create(name="ArticleType 2",
                                                                     accounting_group=self.accounting_group_food, serial_number=False)

    def part_setup_article_type_supplier(self):
        atss = ArticleTypeSupplier.objects.all()
        if len(atss) >=2:
            self.articletypesupplier_article_1 = atss[0]
            self.articletypesupplier_article_2 = atss[1]
        else:
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

    def part_setup_othercosts(self):
        octs = OtherCostType.objects.all()
        if len(octs) >= 2:
            self.othercosttype_1 = octs[0]
            self.othercosttype_2 = octs[1]
        else:
            self.othercosttype_1 = OtherCostType(name="OtherCostType 1", accounting_group=self.accounting_group_components,
                                                 fixed_price=self.price_system_currency_1)
            self.othercosttype_1.save()
            self.othercosttype_2 = OtherCostType(name="OtherCostType 2", accounting_group=self.accounting_group_food,
                                                 fixed_price=self.price_systen_currency_2)
            self.othercosttype_2.save()

    def part_setup_customers(self):
        self.customer_person_1, none = Person.objects.get_or_create(address="Drienerlolaan 5", city="Enschede", email="bestuur@iapc.utwente.nl",
                                        name="Jaap de Steen", phone="0534893927", zip_code="7522NB")
        self.customer_person_2, none = Person.objects.get_or_create(address="Drienerlolaan 5", city="Enschede",
                                        email="schaduwbestuur@iapc.utwente.nl", name="Gerda Steenhuizen",
                                        phone="0534894260", zip_code="7522NB")
        self.organisation, none = Organisation.objects.get_or_create(
                                        address="Drienerlolaan 5", city="Enschede",
                                        email="schaduwbestuur@iapc.utwente.nl", name="Gerda Steenhuizen",
                                        phone="0534894260", zip_code="7522NB")
        self.customer_contact_organisation, none = ContactOrganisation.objects.get_or_create(contact=self.customer_person_1,
                                                                 organisation=self.organisation)

    def part_setup_users(self):
        self.user_1, none = User.objects.get_or_create(username="jsteen")
        self.user_2, none = User.objects.get_or_create(username="ghuis")

    def add_setup_pricing(self):
        pass

    def create_custorders(self, article_1=6, article_2=7, othercost_1=5, othercost_2=8, customer: Customer=None):
        self.CUSTORDERED_ARTICLE_1 = article_1
        self.CUSTORDERED_ARTICLE_2 = article_2
        self.CUSTORDERED_OTHERCOST_1 = othercost_1
        self.CUSTORDERED_OTHERCOST_2 = othercost_2
        if not customer:
            customer = self.customer_person_1
        if article_1 + article_2 + othercost_1 + othercost_2 > 0:
            wish_combs = []
            if article_1 > 0:
                wish_combs.append([self.articletype_1, self.CUSTORDERED_ARTICLE_1, self.price_system_currency_1])
            if article_2 > 0:
                wish_combs.append([self.articletype_2, self.CUSTORDERED_ARTICLE_2, self.price_systen_currency_2])
            if othercost_1 > 0:
                wish_combs.append([self.othercosttype_1, self.CUSTORDERED_OTHERCOST_1, self.price_system_currency_1])
            if othercost_2 > 0:
                wish_combs.append([self.othercosttype_2, self.CUSTORDERED_OTHERCOST_2, self.price_systen_currency_2])
            return Order.create_order_from_wishables_combinations(user=self.user_1, customer=customer,
                                                           wishable_type_number_price_combinations=wish_combs)

    def create_stockwish(self, article_1=6, article_2=7):
        self.STOCKWISHED_ARTICLE_1 = article_1
        self.STOCKWISHED_ARTICLE_2 = article_2
        if article_1 + article_2 > 0:
            art_wishes = []
            if article_1 > 0:
                art_wishes.append([self.articletype_1, self.STOCKWISHED_ARTICLE_1])
            if article_2 > 0:
                art_wishes.append([self.articletype_2, self.STOCKWISHED_ARTICLE_2])
            StockWish.create_stock_wish(user_modified=self.user_1, articles_ordered=art_wishes)

    def create_suporders(self, article_1=4, article_2=5):
        self.SUPPLIERORDERED_ARTICLE_1 = article_1
        self.SUPPLIERORDERED_ARTICLE_2 = article_2
        if article_1 + article_2 > 0:
            arts_ordered = []
            if article_1 > 0:
                arts_ordered.append([self.articletype_1, self.SUPPLIERORDERED_ARTICLE_1, self.cost_system_currency_1])
            if article_2 > 0:
                arts_ordered.append([self.articletype_2, self.SUPPLIERORDERED_ARTICLE_2, self.cost_system_currency_2])
            SupplierOrder.create_supplier_order(user_modified=self.user_1, supplier=self.supplier_1,
                                                articles_ordered=arts_ordered)

    def create_packingdocuments(self, article_1=3, article_2=4):
        self.PACKING_ARTICLE_1 = article_1
        self.PACKING_ARTICLE_2 = article_2
        atccs = []
        if article_1 + article_2 > 0:
            if article_1 > 0:
                atccs.append([self.articletype_1, self.PACKING_ARTICLE_1])
            if article_2 > 0:
                atccs.append([self.articletype_2, self.PACKING_ARTICLE_2])
        if atccs:
            PackingDocument.create_packing_document(supplier=self.supplier_1,
                                                    packing_document_name="Packing document name 1", user=self.user_1,
                                                    article_type_cost_combinations=atccs)

    def create_transactions_article_type_for_order(self, article_1=2, article_2=3, othercost_1=4, order=1):
        self.SOLD_ARTICLE_1 = article_1
        self.SOLD_ARTICLE_2 = article_2
        self.SOLD_OTHERCOST_1 = othercost_1
        if article_1 + article_2 + othercost_1 > 0:
            if not self.register_3.is_open():
                self.register_3.open(counted_amount=Decimal(0))
            if article_1 > 0:
                tl_1 = SalesTransactionLine(price=self.price_system_currency_1, count=self.SOLD_ARTICLE_1, order=order,
                                            article=self.articletype_1)
                money_1 = Money(amount=self.price_system_currency_1.amount * self.SOLD_ARTICLE_1, currency=self.price_system_currency_1.currency)
                pymnt_1 = Payment(amount=money_1, payment_type=self.paymenttype_maestro)
                Transaction.create_transaction(user=self.user_1, transaction_lines=[tl_1], payments=[pymnt_1],
                                               customer=None)
            if article_2 > 0:
                tl_2 = SalesTransactionLine(price=self.price_systen_currency_2, count=self.SOLD_ARTICLE_2, order=order,
                                            article=self.articletype_2)
                money_2 = Money(amount=self.price_systen_currency_2.amount * self.SOLD_ARTICLE_2,
                                currency=self.price_systen_currency_2.currency)
                pymnt_2 = Payment(amount=money_2, payment_type=self.paymenttype_maestro)
                Transaction.create_transaction(user=self.user_2, transaction_lines=[tl_2], payments=[pymnt_2],
                                               customer=self.customer_person_1)
            if othercost_1 > 0:
                octl_1 = OtherCostTransactionLine(price=self.price_system_currency_1, count=self.SOLD_OTHERCOST_1,
                                                  other_cost_type=self.othercosttype_1, order=order)
                money_3 = Money(amount=self.price_system_currency_1.amount * self.SOLD_OTHERCOST_1,
                                currency=self.price_system_currency_1.currency)
                pymnt_3 = Payment(amount=money_3, payment_type=self.paymenttype_maestro)
                Transaction.create_transaction(user=self.user_2, payments=[pymnt_3], transaction_lines=[octl_1],
                                               customer=self.customer_person_2)

    def create_transaction_cash(self, othercost_1=5, othercost_2=7):
        self.sold_othercost_1_cash=othercost_1
        self.sold_othercost_2_cash=othercost_2
        if othercost_1+othercost_2 > 2:
            if not self.register_1.is_open():
                self.register_1.open(counted_amount=Decimal(0), denominations=[])
            if othercost_1 > 0:
                octl_1 = OtherCostTransactionLine(price=self.price_system_currency_1, count=self.sold_othercost_1_cash,
                                                  other_cost_type=self.othercosttype_1, order=None)
                money_3 = Money(amount=self.price_system_currency_1.amount * self.sold_othercost_1_cash,
                                currency=self.price_system_currency_1.currency)
                pymnt_3 = Payment(amount=money_3, payment_type=self.paymenttype_cash)
                Transaction.create_transaction(user=self.user_2, payments=[pymnt_3], transaction_lines=[octl_1],
                                               customer=self.customer_person_2)
            if othercost_2:
                octl_1 = OtherCostTransactionLine(price=self.price_system_currency_1, count=self.sold_othercost_2_cash,
                                                  other_cost_type=self.othercosttype_2, order=None)
                money_3 = Money(amount=self.price_system_currency_1.amount * self.sold_othercost_2_cash,
                                currency=self.price_system_currency_1.currency)
                pymnt_3 = Payment(amount=money_3, payment_type=self.paymenttype_cash)
                Transaction.create_transaction(user=self.user_2, payments=[pymnt_3], transaction_lines=[octl_1],
                                               customer=self.customer_person_2)

    def create_externalisation(self, article_1=5, article_2=7):
        self.INTERNALISED_ARTICLE_1 = article_1
        self.INTERNALISED_ARTICLE_2 = article_2
        if article_1 + article_2 > 0:
            art_list = []
            if article_1 > 0:
                art_list.append((self.articletype_1, article_1, self.cost_system_currency_1))
            if article_2 > 0:
                art_list.append((self.articletype_2, article_2, self.cost_system_currency_2))

            ExternaliseDocument.create_external_products_document(user=self.user_1, article_information_list=art_list,
                                                                  memo="Testing tool externalisation")


class TestMixins(TestCase, TestData):

    def test_all_in_sequence(self):
        self.setup_base_data()
        self.add_setup_pricing()
        order = self.create_custorders()
        self.create_suporders()
        self.create_stockwish()
        self.create_packingdocuments()
        self.create_transactions_article_type_for_order(article_1=2, article_2=3, othercost_1=4, order=order.id)
        self.create_externalisation()

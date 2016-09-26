from django.test import TestCase



def _assert(truthvalue, errorstring=None):
    if not truthvalue:
        raise AssertionError(errorstring)


class TestData(TestCase):

    def setup_base_data(self):
        from money.models import VAT, Currency, AccountingGroup, Denomination, Cost, Price, CurrencyData
        from article.models import AssortmentArticleBranch, ArticleType, OtherCostType
        from register.models import PaymentType, Register
        from decimal import Decimal
        from crm.models import User, Person
        from supplier.models import Supplier, ArticleTypeSupplier

        self.currency_data_eur = CurrencyData(iso="EUR", name="Euro", symbol="€", digits=2)
        self.currency_data_eur.save()
        self.currency_data_usd = CurrencyData(iso="USD", name="US Dollar", symbol="$", digits=2)
        self.currency_data_usd.save()

        self.vat_group_high = VAT(vatrate=1.21, name="High", active=True)
        self.vat_group_high.save()
        self.vat_group_low = VAT(vatrate=1.06, name="Low", active=True)
        self.vat_group_low.save()

        self.currency_eur = Currency(iso="EUR")
        self.currency_usd = Currency(iso="USD")

        self.accounting_group_components = AccountingGroup(name="Components", vat_group=self.vat_group_high, accounting_number=1)
        self.accounting_group_components.save()
        self.accounting_group_food = AccountingGroup(name="Food", vat_group=self.vat_group_low, accounting_number=2)
        self.accounting_group_food.save()

        self.branch_1 = AssortmentArticleBranch(name="First Branch", parent_tag=None)
        self.branch_1.save()
        self.branch_2 = AssortmentArticleBranch(name="Second Branch", parent_tag=self.branch_1)
        self.branch_2.save()

        self.paymenttype_cash = PaymentType(name="Cash")
        self.paymenttype_cash.save()
        self.paymenttype_maestro = PaymentType(name="Maestro")
        self.paymenttype_maestro.save()

        self.register_1 = Register(currency=self.currency_data_eur, is_cash_register=True, payment_type=self.paymenttype_cash)
        self.register_2 = Register(currency=self.currency_data_eur, is_cash_register=True, payment_type=self.paymenttype_cash)
        self.register_1.save()
        self.register_2.save()

        self.denomination_eur_20 = Denomination(currency=self.currency_data_eur, amount=20)
        self.denomination_eur_20.save()
        self.denomination_eur_0_01 = Denomination(currency=self.currency_data_eur, amount=0.01)
        self.denomination_eur_0_01.save()

        self.price_eur_1 = Price(amount=Decimal(1.23), currency=self.currency_eur, vat=1.21)
        self.price_eur_2 = Price(amount=Decimal(2.10), currency=self.currency_eur, vat=1.06)

        self.cost_eur_1 = Cost(amount=Decimal(1.23), currency=self.currency_eur)
        self.cost_eur_2 = Cost(amount=Decimal(2.10), currency=self.currency_eur)

        self.supplier_1 = Supplier(name="Supplier 1")
        self.supplier_1.save()
        self.supplier_2 = Supplier(name="Supplier 2")
        self.supplier_2.save()

        self.articletype_1 = ArticleType(name="ArticleType 1", accounting_group=self.accounting_group_components, branch=self.branch_1)
        self.articletype_1.save()
        self.articletype_2 = ArticleType(name="ArticleType 2", accounting_group=self.accounting_group_food, branch=self.branch_2)
        self.articletype_2.save()

        self.articletypesupplier_article_1 = ArticleTypeSupplier(supplier=self.supplier_1, article_type=self.articletype_1, cost=self.cost_eur_1, availability='A', supplier_string="SupplierArticleType 1", minimum_number_to_order=1)
        self.articletypesupplier_article_1.save()
        self.articletypesupplier_article_2 = ArticleTypeSupplier(supplier=self.supplier_1, article_type=self.articletype_2, cost=self.cost_eur_2, availability='A', supplier_string="SupplierArticleType 2", minimum_number_to_order=1)
        self.articletypesupplier_article_2.save()

        self.othercosttype_1 = OtherCostType(name="OtherCostType 1", accounting_group=self.accounting_group_components, branch=self.branch_1, fixed_price=self.price_eur_1)
        self.othercosttype_1.save()
        self.othercosttype_2 = OtherCostType(name="OtherCostType 2", accounting_group=self.accounting_group_food, branch=self.branch_2, fixed_price=self.price_eur_2)
        self.othercosttype_2.save()

        self.customer_person_1 = Person(address="Drienerlolaan 5", city="Enschede", email="bestuur@iapc.utwente.nl",
                                        name="Jaap de Steen", phone="0534893927", zip_code="7522NB")
        self.customer_person_1.save()
        self.customer_person_2 = Person(address="Drienerlolaan 5", city="Enschede", email="schaduwbestuur@iapc.utwente.nl",
                                           name="Gerda Steenhuizen", phone="0534894260", zip_code="7522NB")
        self.customer_person_2.save()

        self.user_1 = User(username="jsteen")
        self.user_1.save()
        self.user_2 = User(username="ghuis")
        self.user_2.save()

    def create_custorders(self, article_1=6, article_2=7, othercost_1=5, othercost_2=8):
        from order.models import Order
        self.CUSTORDERED_ARTICLE_1 = article_1
        self.CUSTORDERED_ARTICLE_2 = article_2
        self.CUSTORDERED_OTHERCOST_1 = othercost_1
        self.CUSTORDERED_OTHERCOST_2 = othercost_2
        Order.create_order_from_wishables_combinations(user=self.user_1, customer=self.customer_person_1,
                                                       wishable_type_number_price_combinations=[
                                                           [self.articletype_1, self.CUSTORDERED_ARTICLE_1, self.price_eur_1],
                                                           [self.articletype_2, self.CUSTORDERED_ARTICLE_2, self.price_eur_2],
                                                       [self.othercosttype_1, self.CUSTORDERED_OTHERCOST_1, self.price_eur_1],
                                                       [self.othercosttype_2, self.CUSTORDERED_OTHERCOST_2, self.price_eur_2]])

    def create_suporders(self, article_1=4, article_2=5):
        from logistics.models import SupplierOrder
        self.SUPPLIERORDERED_ARTICLE_1 = article_1
        self.SUPPLIERORDERED_ARTICLE_2 = article_2
        SupplierOrder.create_supplier_order(user_modified=self.user_1, supplier=self.supplier_1,
                                            articles_ordered=[[self.articletype_1, self.SUPPLIERORDERED_ARTICLE_1, self.cost_eur_1],
                                                              [self.articletype_2, self.SUPPLIERORDERED_ARTICLE_2, self.cost_eur_2]])

    def create_packingdocuments(self, article_1=3, article_2=4):
        from supplication.models import PackingDocument
        self.PACKING_ARTICLE_1 = article_1
        self.PACKING_ARTICLE_2 = article_2
        PackingDocument.create_packing_document(supplier=self.supplier_1, packing_document_name="Packing document name 1", user=self.user_1,
                                                article_type_cost_combinations=[[self.articletype_1, self.PACKING_ARTICLE_1], [self.articletype_2, self.PACKING_ARTICLE_2]])


from django.db import models, transaction
from supplier.models import Supplier, ArticleTypeSupplier
from order.models import OrderLine, OrderCombinationLine
from crm.models import User
from article.models import ArticleType, OrProductType


class SupplierOrder(models.Model):
    """
    Order we place at a supplier
    """
    supplier = models.ForeignKey(Supplier)

    copro = models.ForeignKey(User)

    @staticmethod
    def create_supplier_order(user, article_type_number_combos):
        ARTICLE_TYPE_LOCATION = 0
        NUMBER_LOCATION = 1
        assert user and article_type_number_combos
        assert isinstance(user, User)
        assert len(article_type_number_combos) > 0

        # Check if there not more supply than demand

        article_type_supply = {}

        for atnc in article_type_number_combos:
            assert isinstance(atnc[ARTICLE_TYPE_LOCATION], ArticleType)
            assert isinstance(atnc[NUMBER_LOCATION], int)
            assert atnc[NUMBER_LOCATION] > 0
            if article_type_supply.get(atnc[ARTICLE_TYPE_LOCATION]) is None:
                article_type_supply[atnc[ARTICLE_TYPE_LOCATION]] = atnc[NUMBER_LOCATION]
            else:
                article_type_supply[atnc[ARTICLE_TYPE_LOCATION]] += atnc[NUMBER_LOCATION]

        article_type_demand = {}
        swls = StockWishLine.objects.all()
        for swl in swls:
            article_type_demand[swl.article_type] = swl.number
        combo_order_lines = OrderCombinationLine.get_ol_combinations(state='O',include_price_field=False)
        for col in combo_order_lines:
            if article_type_demand.get(col.wishable) is None:
                article_type_demand[col.wishable] = col.number
            else:
                article_type_demand[col.wishable] += col.number

        for supply in article_type_supply:
            print("Article "+supply.name)
            if (article_type_demand.get(supply) is None) or \
                    (article_type_demand[supply] < article_type_supply[supply]):
                #print("Demand for article" + supply.name +" is "+ article_type_demand[supply])
                #print("Supply for article" + supply.name +" is "+ article_type_supply[supply])
                #raise InsufficientDemandError()
                pass







class SupplierOrderLine(models.Model):
    """
    Single ArticleType ordered at supplier and contained in a SupplierOrder
    """
    supplier_order = models.ForeignKey(SupplierOrder)

    article_type = models.ForeignKey(ArticleType)

    supplier_article_type = models.ForeignKey(ArticleTypeSupplier)

    order_line = models.ForeignKey(OrderLine, null=True)

    @transaction.atomic
    def save(self):
        if self.order_line is not None:
            if isinstance(self.order_line.wishable, OrProductType):
                raise UnimplementedError("Functionality is not implemented yet")
                # Working Or-products can be very complicated. A matching should be queried and worked out in order
                # for it to work
            else:
                assert self.order_line.wishable == self.article_type # Customer article matches ordered article
        if self.supplier_article_type is None:
            sup_art_types = ArticleTypeSupplier.objects.filter(article_type=self.article_type, supplier=self.supplier_order.supplier)
            if len(sup_art_types) == 1:
                self.supplier_article_type == sup_art_types[0]
        assert self.supplier_article_type.supplier == self.supplier_order.supplier # Article can be ordered at supplier
        assert self.supplier_article_type == ArticleTypeSupplier.objects.get(article_type=self.article_type,
                                                                             supplier=self.supplier_order.supplier)

        # Assert that everything is ok here
        if self.pk is None:
            if self.order_line is not None:
                self.order_line.order_at_supplier()  # If this doesn't happen at exactly the same time
                                                     # as the save of the SupOrdLn, you are screwed
            super(SupplierOrderLine, self).save()
        else:
            # Maybe some extra logic here?
            super(SupplierOrderLine, self).save()


class StockWishLine(models.Model):
    """
    Single line that indicates the wish for a certain number of ArticleTypes. Can be negative for obsolete wishes.
    """

    article_type = models.ForeignKey(ArticleType)

    number = models.IntegerField()

    stock_wish = models.ForeignKey('StockWish')

    def save(self):
        assert self.number is not 0
        assert self.stock_wish is not None  # Pre-check, assumed present from here on out
        if self.pk is None:
            if self.number > 0:
                StockWishTable.add_products_to_table(self.article_type, self.number, indirect=True,
                                                     stock_wish=self.stock_wish)
            else:
                StockWishTable.remove_products_from_table(self.article_type, -1 * self.number, indirect=True,
                                                          stock_wish=self.stock_wish)
            super(StockWishLine, self).save()
        # Immutable after storage to prevent backlogging


class StockWish(models.Model):
    """
    Combination of wishes for ArticleTypes to be ordered at supplier.
    """

    copro = models.ForeignKey(User)

    timestamp = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def create_stock_wish(user, article_type_number_combos):
        """
        Creates stock wishes integrally, this function is the preferred way of creating stock wishes
        :param user: User to be connected to the stockwish
        :param article_type_number_combos: lists containing both ArticleTypes and a non-zero integer
        :return:
        """
        ARTICLE_TYPE_LOCATION = 0
        NUMBER_LOCATION = 1
        # Validity checks
        assert user and article_type_number_combos
        assert isinstance(user, User)
        assert len(article_type_number_combos) > 0
        for atnc in article_type_number_combos:
            assert isinstance(atnc[ARTICLE_TYPE_LOCATION], ArticleType)
            assert isinstance(atnc[NUMBER_LOCATION], int)
            assert atnc[NUMBER_LOCATION] is not 0

        stock_wish = StockWish(copro=user)
        stock_wish.save()
        for atnc in article_type_number_combos:
            swl = StockWishLine(article_type=atnc[ARTICLE_TYPE_LOCATION], number=atnc[NUMBER_LOCATION],
                                stock_wish=stock_wish)
            swl.save()


class StockWishTableLine(models.Model):
    """
    Single line of all combined present wishes for a single ArticleType. Will be modified by StockWishes
    and SupplierOrders.
    """

    article_type = models.OneToOneField(ArticleType)

    number = models.IntegerField()

    def save(self, indirect=False):
        if not indirect:
            raise IndirectionError("StockWishTableLine must be called indirectly from StockWishTable")
        else:
            super(StockWishTableLine, self).save()


class StockWishTable:
    """
    Helper methods for creating Stock Wishes. Let functions that modify the stock wish table call these functions
    """

    @staticmethod
    def add_products_to_table(article_type, number, indirect=False,
                              stock_wish=None, supplier_order=None):
        if not indirect:
            raise IndirectionError("add_products_to_table must be called indirectly")
        article_type_status = StockWishTableLine.objects.filter(article_type=article_type)
        if len(article_type_status) == 0:
            swtl = StockWishTableLine(article_type=article_type, number=number)
            swtl.save(indirect=indirect)
            log = StockWishTableLog(number=number, article_type=article_type,
                                    stock_wish=stock_wish, supplier_order=supplier_order)
            log.save(indirect=True)
        else:
            article_type_status[0].number += number
            article_type_status[0].save(indirect=indirect)
            log = StockWishTableLog(number=number, article_type=article_type,
                                    stock_wish=stock_wish, supplier_order=supplier_order)
            log.save(indirect=True)

    @staticmethod
    def remove_products_from_table(article_type, number, indirect=False,
                                   stock_wish=False, supplier_order=None):
        if not indirect:
            raise IndirectionError("remove_products_from_table must be called indirectly")
        article_type_status = StockWishTableLine.objects.get(article_type=article_type)
        if len(article_type_status) == 0:
            raise CannotRemoveFromWishTableError("ArticleType is not included in table")
        else:
            if article_type_status[0].number < number:
                raise CannotRemoveFromWishTableError("Less ArticleTypes present than removal number")
            else:
                article_type_status[0].number -= number
                article_type_status[0].save(indirect=indirect)
                log = StockWishTableLog(number=-number, article_type=article_type,
                                        stock_wish=stock_wish, supplier_order=supplier_order)
                log.save(indirect=True)


class StockWishTableLog(models.Model):
    """
    Log of all edits of the stock wish.
    """

    number = models.IntegerField()

    article_type = models.ForeignKey(ArticleType)

    supplier_order = models.ForeignKey(SupplierOrder, null=True)

    stock_wish = models.ForeignKey(StockWish, null=True)

    def save(self, indirect=False):
        if not indirect:
            raise IndirectionError("Saving must be done indirectly")
        assert (self.supplier_order or self.stock_wish) and not(self.supplier_order and self.stock_wish)
        # ^ reason is either supplier order or stock wish modification
        assert self.pk is None  # No edits after creation
        super(StockWishTableLog, self).save()


class UnimplementedError(Exception):
    pass


class CannotRemoveFromWishTableError(Exception):
    pass


class IndirectionError(Exception):
    pass


class InsufficientDemandError(Exception):
    pass

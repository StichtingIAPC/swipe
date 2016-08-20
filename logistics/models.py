from collections import defaultdict

from django.db import models, transaction
from supplier.models import Supplier, ArticleTypeSupplier
from order.models import OrderLine, OrderCombinationLine
from crm.models import User
from article.models import ArticleType, OrProductType
from swipe.settings import USED_STRATEGY


class SupplierOrder(models.Model):
    """
    Order we place at a supplier
    """
    supplier = models.ForeignKey(Supplier)

    copro = models.ForeignKey(User)

    @staticmethod
    def create_supplier_order(user, supplier, articles_ordered=None):
        """
        Checks if supplier order information is correct and orders it at the correct supplier
        :param user: user to which the order is authorized
        :param supplier: supplier which should order the products
        :param articles_ordered:
        :type articles_ordered: List[Tuple[ArticleType, int]]
        :return:
        """

        assert user and articles_ordered
        assert isinstance(user, User)
        assert articles_ordered
        # is same as assert len(articles_ordered, but

        # Ensure that the number of articles ordered is not less than 0

        ordered_dict = defaultdict(lambda: 0)

        for article, number in articles_ordered:
            assert isinstance(article, ArticleType)
            assert isinstance(number, int)
            assert number > 0
            ordered_dict[article] += number
            assert ArticleTypeSupplier.objects.get(article_type=article) #  Article exists at supplier

        demand_errors = SupplierOrder.verify_article_demand(ordered_dict)

        if demand_errors:
            err_msg = "Not enough demand for ordered articles: \n"
            for article, number in demand_errors:
                err_msg += \
                    " - Article {article} was ordered {number} times, " \
                    "but only {valid_number} were accounted for. \n".format(
                        article=article.name,
                        number=ordered_dict[article],
                        valid_number=ordered_dict[article]-number
                    )
            raise InsufficientDemandError(err_msg)

        # Create supplier order and modify customer orders
        distribution = DisbributionStrategy.get_strategy_from_string(USED_STRATEGY)\
            .get_distribution(user, supplier,
                              articles_ordered)

        DisbributionStrategy.distribute(user, supplier, distribution, indirect=True)



    @staticmethod
    def verify_article_demand(articles_ordered=None):
        """
        :param articles_ordered:
        :type articles_ordered: Dict[ArticleType, int]
        :return: List[Tuple[ArticleType, int]]
        """
        assert articles_ordered

        errors = []

        to_order = defaultdict(lambda: 0)

        stockwish_table_lines = StockWishTableLine.objects.all()

        for line in stockwish_table_lines:
            to_order[line.article_type] += line.number

        combo_order_lines = OrderCombinationLine.get_ol_combinations(state='O', include_price_field=False)

        for line in combo_order_lines:
            if not hasattr(line.wishable, 'sellabletype') or \
                            line.wishable.sellabletype is None:
                raise UnimplementedError("Or products are not yet supported")

            to_order[line.wishable.sellabletype.articletype] += line.number

        for article, number in articles_ordered.items():
            if to_order[article] < articles_ordered[article]:
                errors.append((article, number - to_order[article]))

        return errors


class SupplierOrderLine(models.Model):
    """
    Single ArticleType ordered at supplier and contained in a SupplierOrder
    """
    supplier_order = models.ForeignKey(SupplierOrder)

    article_type = models.ForeignKey(ArticleType)

    supplier_article_type = models.ForeignKey(ArticleTypeSupplier)

    order_line = models.ForeignKey(OrderLine, null=True)

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.order_line is not None:
            if isinstance(self.order_line.wishable, OrProductType):
                assert ArticleType.objects.filter(
                    orproducttype__id=self.order_line.id,
                    id=self.article_type.id).exists()
            else:
                assert self.order_line.wishable == self.article_type # Customer article matches ordered article
        if self.supplier_article_type is None:
            sup_art_types = ArticleTypeSupplier.objects.filter(
                article_type=self.article_type,
                supplier=self.supplier_order.supplier)

            assert len(sup_art_types) == 1
            self.supplier_article_type == sup_art_types[0]

        assert self.supplier_article_type.supplier == self.supplier_order.supplier # Article can be ordered at supplier
        assert self.supplier_article_type == ArticleTypeSupplier.objects.get(
            article_type=self.article_type,
            supplier=self.supplier_order.supplier)

        # Assert that everything is ok here
        if self.pk is None:
            if self.order_line is not None:
                self.order_line.order_at_supplier()  # If this doesn't happen at exactly the same time
                                                     # as the save of the SupOrdLn, you are screwed
            super(SupplierOrderLine, self).save(*args, **kwargs)
        else:
            # Maybe some extra logic here?
            super(SupplierOrderLine, self).save(*args, **kwargs)


class StockWish(models.Model):
    """
    Combination of wishes for ArticleTypes to be ordered at supplier.
    """

    copro = models.ForeignKey(User)

    timestamp = models.DateTimeField(auto_now_add=True)

    @staticmethod
    @transaction.atomic
    def create_stock_wish(user=None, articles_ordered=None):
        """
        Creates stock wishes integrally, this function is the preferred way of creating stock wishes
        :param user: User to be connected to the stockwish
        :type user: User
        :param articles_ordered: tuples containing both ArticleTypes and a non-zero integer
        :type articles_ordered:
        :return:
        """

        assert user is not None and len(articles_ordered) > 0
        assert isinstance(user, User)

        for article, number in articles_ordered:
            assert isinstance(article, ArticleType)
            assert isinstance(number, int)
            assert number != 0

        stock_wish = StockWish(copro=user)
        stock_wish.save()

        for article, number in articles_ordered:
            if number < 0:
                StockWishTable.remove_products_from_table(
                    article,
                    -number,
                    indirect=True,
                    stock_wish=stock_wish,
                    supplier_order=None
                )
            else:
                StockWishTable.add_products_to_table(
                    article,
                    number,
                    indirect=True,
                    stock_wish=stock_wish,
                    supplier_order=None
                )
        return stock_wish


class StockWishTableLine(models.Model):
    """
    Single line of all combined present wishes for a single ArticleType. Will be modified by StockWishes
    and SupplierOrders.
    """

    article_type = models.OneToOneField(ArticleType)

    number = models.IntegerField(default=0)

    def save(self, indirect=False, *args, **kwargs):
        if not indirect:
            raise IndirectionError("StockWishTableLine must be called indirectly from StockWishTable")
        else:
            super(StockWishTableLine, self).save(*args, **kwargs)


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
            log = StockWishTableLog(
                number=number,
                article_type=article_type,
                stock_wish=stock_wish,
                supplier_order=supplier_order)
            log.save(indirect=True)
        else:
            article_type_status[0].number += number
            article_type_status[0].save(indirect=indirect)
            log = StockWishTableLog(
                number=number,
                article_type=article_type,
                stock_wish=stock_wish,
                supplier_order=supplier_order)
            log.save(indirect=True)

    @staticmethod
    def remove_products_from_table(article_type, number, indirect=False,
                                   stock_wish=False, supplier_order=None):
        if not indirect:
            raise IndirectionError("remove_products_from_table must be called indirectly")
        article_type_statuses = StockWishTableLine.objects.filter(article_type=article_type)
        if not article_type_statuses:
            return
        article_type_status = article_type_statuses[0]
        if article_type_status.number - number < 0:
            raise CannotRemoveFromWishTableError("Less ArticleTypes present than removal number")
        else:
            article_type_status.number -= number
            article_type_status.save(indirect=indirect)
            log = StockWishTableLog(
                number=-number,
                article_type=article_type,
                stock_wish=stock_wish,
                supplier_order=supplier_order)
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


class DisbributionStrategy():

    @staticmethod
    def get_strategy_from_string(strategy):
        if strategy == "IndiscriminateCustomerStockStrategy":
            return IndiscriminateCustomerStockStrategy
        else:
            raise UnimplementedError("Strategy not implemented")

    @staticmethod
    @transaction.atomic()
    def distribute(user, supplier, distribution, indirect=False):
        """
        Creates the supplier order and distributes the SupplierOrderLines to any orders
        :param user: a User for the SupplierOrder
        :param supplier: Supplier for the SupplierOrder
        :param distribution: A list of Tuples containing SupplierOrderLines and OrderLines(possibly None)
        :param indirect: Indirection flag. Function must be called indirectly.
        """
        assert isinstance(user, User)
        assert isinstance(supplier, Supplier)
        if not indirect:
            raise IndirectionError("Distribute must be called indirectly")
        supplier_order = SupplierOrder(copro=user, supplier=supplier)
        for supplier_order_line, order_line in distribution:
            assert isinstance(supplier_order_line, SupplierOrderLine)
            assert order_line is None or isinstance(order_line, OrderLine)
            supplier_order_line.order_line = order_line
            if isinstance(order_line, OrderLine):
                assert supplier_order_line.article_type == order_line.wishable.sellabletype.articletype

        # We've checked everyting, now we start saving
        supplier_order.save()
        for supplier_order_line, order_line in distribution:
            supplier_order_line.supplier_order = supplier_order
            supplier_order_line.save()

    @staticmethod
    def get_distribution(article_type_number_combos):
        """
        Proposes a distribution according to the specific strategy.
        :param article_type_number_combos:
        :return: A list of Tuples containing SupplierOrderLines and OrderLines(possibly None)
        """
        return []


class IndiscriminateCustomerStockStrategy(DisbributionStrategy):

    @staticmethod
    def get_distribution(article_type_number_combos):
        distribution = []
        articletype_dict = {}
        for articletype, number in article_type_number_combos:
            articletype_dict[articletype] = True
        articletypes = articletype_dict.keys()
        relevant_orderlines = OrderLine.objects.filter(state='O', wishable__in=articletypes)
        # Match the orders one-by-one, stopping when all orders and wishes are fulfilled or article from the
        # article type number combos run out

        return distribution


class UnimplementedError(Exception):
    pass


class CannotRemoveFromWishTableError(Exception):
    pass


class IndirectionError(Exception):
    pass


class InsufficientDemandError(Exception):
    pass

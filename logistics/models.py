from collections import defaultdict
from decimal import Decimal
from django.db import models, transaction
from django.db.models import Count
from django.db.models.fields.reverse_related import ForeignObjectRel


from blame.models import ImmutableBlame, Blame
from supplier.models import Supplier, ArticleTypeSupplier
from order.models import OrderLine, OrderCombinationLine
from crm.models import User
from article.models import ArticleType, OrProductType
from swipe.settings import USED_STRATEGY, USED_CURRENCY
from money.models import CostField, Cost, Currency


class SupplierOrder(ImmutableBlame):
    """
    Order we place at a supplier
    """
    supplier = models.ForeignKey(Supplier)


    def __str__(self):
        return "Supplier: {}, User: {}".format(self.supplier, self.user_created)

    @staticmethod
    def create_supplier_order(user_modified, supplier, articles_ordered=None, allow_different_currency=False):
        """
        Checks if supplier order information is correct and orders it at the correct supplier
        :param user: user to which the order is authorized
        :param supplier: supplier which should order the products
        :param articles_ordered:
        :type articles_ordered: List[List[ArticleType, int, Cost]]
        :param allow_different_currency: If true, removes checks for the currency to see if its the system currency
        """

        ordered_dict = SupplierOrder.verify_data_assertions(user_modified, supplier, articles_ordered, allow_different_currency)

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
            .get_distribution(articles_ordered)

        DisbributionStrategy.distribute(user_modified, supplier, distribution, indirect=True)

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

    @staticmethod
    def verify_data_assertions(user, supplier, articles_ordered, allow_different_currency):
        """
        Checks basic assertions about the supplied data, including the supplier ability to supply the specified products
        :param user: user to which the order is authorized
        :param supplier: supplier which should order the products
        :param articles_ordered:
        :type articles_ordered: List[List[ArticleType, int]]
        """
        assert user and articles_ordered
        assert isinstance(user, User)
        assert articles_ordered
        # is same as assert len(articles_ordered, but

        # Ensure that the number of articles ordered is not less than 0

        ordered_dict = defaultdict(lambda: 0)

        for article, number, cost in articles_ordered:
            assert isinstance(article, ArticleType)
            assert isinstance(number, int)
            assert isinstance(cost, Cost)
            if not allow_different_currency:
                assert cost.currency.iso == USED_CURRENCY
            assert number > 0
            ordered_dict[article] += number
            assert ArticleTypeSupplier.objects.get(article_type=article,
                                                   supplier=supplier)  # Article exists at supplier
        return ordered_dict


class SupplierOrderLine(Blame):
    """
    Single ArticleType ordered at supplier and contained in a SupplierOrder
    """
    supplier_order = models.ForeignKey(SupplierOrder)

    article_type = models.ForeignKey(ArticleType)

    supplier_article_type = models.ForeignKey(ArticleTypeSupplier)

    order_line = models.ForeignKey(OrderLine, null=True)

    line_cost = CostField()

    state = models.CharField(max_length=5)

    def __str__(self):
        if not hasattr(self, 'supplier_order')or self.supplier_order is None:
            supplier_order = "None"
        else:
            supplier_order = self.supplier_order.pk
        if not hasattr(self, 'article_type') or self.article_type is None:
            article_type = "None"
        else:
            article_type = str(self.article_type)
        if not hasattr(self, 'supplier_article_type') or self.supplier_article_type is None:
            supplier_article_type = "None"
        else:
            supplier_article_type = str(self.supplier_article_type.pk)
        if not hasattr(self, 'order_line') or self.order_line is None:
            order_line = "None"
        else:
            order_line = str(self.order_line.pk)
        if not hasattr(self, 'line_cost') or self.line_cost is None:
            line_cost = "None"
        else:
            line_cost = str(self.line_cost)
        if not hasattr(self, 'state') or self.state is None:
            state = "None"
        else:
            state = self.state

        stri = "SupplierOrder: {}, ArticleType: {}, " \
               "SupplierArticleType: {}, OrderLine: {}, Cost: {}, State: {}".format(supplier_order,
                                                                                    article_type,
                                                                                    supplier_article_type,
                                                                                    order_line, line_cost, state)
        return stri

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.order_line is not None:
            if isinstance(self.order_line.wishable, OrProductType):
                assert ArticleType.objects.filter(
                    orproducttype__id=self.order_line.id,
                    id=self.article_type.id).exists()
            else:
                assert self.order_line.wishable.sellabletype.articletype == self.article_type  # Customer article matches ordered article
        checked_ats = False
        if not hasattr(self, 'supplier_article_type') or self.supplier_article_type is None:
            sup_art_types = ArticleTypeSupplier.objects.filter(
                article_type=self.article_type,
                supplier=self.supplier_order.supplier)
            checked_ats = True

            assert len(sup_art_types) == 1
            self.supplier_article_type == sup_art_types[0]

        if not checked_ats:
            assert self.supplier_article_type.supplier == self.supplier_order.supplier  # Article can be ordered at supplier
            assert self.supplier_article_type == ArticleTypeSupplier.objects.get(
                article_type=self.article_type,
                supplier=self.supplier_order.supplier)

        # Set the relevant state is not implemented
        if self.pk is None:
            self.state = 'O'
        assert self.state in SupplierOrderState.STATE_CHOICES
        # Assert that everything is ok here
        if self.pk is None:
            if self.order_line is not None:
                self.order_line.order_at_supplier(self.supplier_order.user_created)  # If this doesn't happen at exactly the same time
                                                     # as the save of the SupOrdLn, you are screwed
            else:
                StockWishTable.remove_products_from_table(self.user_modified, article_type=self.article_type, number=1,
                                                          supplier_order=self.supplier_order, stock_wish=None, indirect=True)
            super(SupplierOrderLine, self).save(*args, **kwargs)
            sos = SupplierOrderState(supplier_order_line=self, state=self.state,user_modified=self.user_modified)
            sos.save()
        else:
            # Maybe some extra logic here?
            super(SupplierOrderLine, self).save(*args, **kwargs)

    @transaction.atomic()
    def transition(self, new_state, user_modified):
        """
        Transitions an orderline from one state to another. This is the only safe means of transitioning, as data
        integrity can not be guaranteed otherwise. Transitioning is only possible with objects stored in the database.
        """
        if not self.pk or self.state is None:
            raise ObjectNotSavedError()
        elif self.state not in SupplierOrderState.STATE_CHOICES:
            raise IncorrectStateError("State of orderline is not valid. Database is corrupted at Orderline", self.pk,
                                      " with state ", self.state)
        elif new_state not in SupplierOrderState.STATE_CHOICES:
            raise IncorrectTransitionError("New state is not a valid state")
        else:
            nextstates = {
                   'O': ('B', 'C', 'A'),
                   'B': ('A', 'C')}
            if new_state in nextstates[self.state]:
                self.state = new_state
                self.user_modified = user_modified
                sols = SupplierOrderState(state=new_state, supplier_order_line=self, user_modified=user_modified)
                sols.save()
                self.save()
            else:
                raise IncorrectTransitionError(
                       "This transaction is not legal: {state} -> {new_state}".format(state=self.state,
                                                                                      new_state=new_state))

    def send_to_backorder(self, user_modified):
        self.transition('B', user_modified)

    @transaction.atomic()
    def mark_as_arrived(self, user_modified):
        if self.order_line is not None:
            self.order_line.arrive_at_store(user_modified)
        self.transition('A', user_modified)

    @transaction.atomic
    def cancel_line(self, user_modified, cancel_order=False):
        # Has orderline
        if self.order_line is not None:
            # Either cancel the order outright or revert to basic state
            if cancel_order:
                self.order_line.cancel(user_modified)
            else:
                self.order_line.return_back_to_ordered_by_customer(user_modified)
        else:
            if not cancel_order:
                StockWishTable.add_products_to_table(user_modified=user_modified, number=1,
                                                     indirect=True, article_type=self.article_type,
                                                     supplier_order=self.supplier_order)

        self.transition('C', user_modified)


class SupplierOrderState(ImmutableBlame):

    STATE_CHOICES = ('O', 'B', 'C', 'A')
    STATE_CHOICES_MEANING = {'O': 'Ordered at supplier', 'B': 'Backorder', 'C': 'Cancelled',
                             'A': 'Arrived at store'}

    timestamp = models.DateTimeField(auto_now_add=True)

    supplier_order_line = models.ForeignKey(SupplierOrderLine)

    state = models.CharField(max_length=5)


class StockWish(ImmutableBlame):
    """
    Combination of wishes for ArticleTypes to be ordered at supplier.
    """


    timestamp = models.DateTimeField(auto_now_add=True)

    @staticmethod
    @transaction.atomic
    def create_stock_wish(user_modified, articles_ordered):
        """
        Creates stock wishes integrally, this function is the preferred way of creating stock wishes
        :param user_modified: User to be connected to the stockwish
        :type user_modified: User
        :param articles_ordered: tuples containing both ArticleTypes and a non-zero integer
        :type articles_ordered:
        :return:
        """

        assert user_modified is not None and len(articles_ordered) > 0
        assert isinstance(user_modified, User)

        for article, number in articles_ordered:
            assert isinstance(article, ArticleType)
            assert isinstance(number, int)
            assert number != 0

        stock_wish = StockWish(user_modified=user_modified)
        stock_wish.save()

        for article, number in articles_ordered:
            if number < 0:
                StockWishTable.remove_products_from_table(user_modified,
                    article,
                    -number,
                    indirect=True,
                    stock_wish=stock_wish,
                    supplier_order=None
                )
            else:
                StockWishTable.add_products_to_table(
                    user_modified,
                    article,
                    number,
                    indirect=True,
                    stock_wish=stock_wish,
                    supplier_order=None
                )
        return stock_wish


class StockWishTableLine(Blame):
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
    def add_products_to_table(user_modified, article_type, number, indirect=False,
                              stock_wish=None, supplier_order=None):
        assert number > 0
        if not indirect:
            raise IndirectionError("add_products_to_table must be called indirectly")
        article_type_status = StockWishTableLine.objects.filter(article_type=article_type)
        if len(article_type_status) == 0:
            swtl = StockWishTableLine(article_type=article_type, number=number, user_modified=user_modified)
            swtl.save(indirect=indirect)
            log = StockWishTableLog(
                number=number,
                article_type=article_type,
                stock_wish=stock_wish,
                supplier_order=supplier_order,  user_modified=user_modified)
            log.save(indirect=True)
        else:
            article_type_status[0].number += number
            article_type_status[0].save(indirect=indirect)
            log = StockWishTableLog(
                number=number,
                article_type=article_type,
                stock_wish=stock_wish,
                supplier_order=supplier_order, user_modified=user_modified)
            log.save(indirect=True)

    @staticmethod
    def remove_products_from_table(user_modified,article_type, number, indirect=False,
                                   stock_wish=None, supplier_order=None):
        assert number > 0
        if not indirect:
            raise IndirectionError("remove_products_from_table must be called indirectly")
        article_type_statuses = StockWishTableLine.objects.filter(article_type=article_type)
        if not article_type_statuses:
            return
        article_type_status = article_type_statuses[0]
        if article_type_status.number - number < 0:
            raise CannotRemoveFromWishTableError("Less ArticleTypes present than removal number")
        else:
            if article_type_status.number - number == 0:
                article_type_status.delete()
            else:
                article_type_status.number -= number
                article_type_status.save(indirect=indirect)

            log = StockWishTableLog(
                number=-number,
                article_type=article_type,
                stock_wish=stock_wish,
                supplier_order=supplier_order,user_modified=user_modified)
            log.save(indirect=True)


class StockWishTableLog(ImmutableBlame):
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

    def __str__(self):
        if self.supplier_order is None:
            sup_ord = "None"
        else:
            sup_ord = self.supplier_order.pk
        if self.stock_wish is None:
            stw = "None"
        else:
            stw = self.stock_wish.pk
        return "{} x {}, SupplierOrder: {}, StockWish: {}".format(self.article_type, self.number, sup_ord, stw)

class SupplierOrderCombinationLine:

    number = 0

    article_type = ArticleType

    cost = CostField

    state = ""

    def __init__(self, number, article_type, cost, state):
        self.number = number
        self.article_type = article_type
        self.cost = cost
        self.state = state

    def __str__(self):
        dec = self.cost.amount.quantize(Decimal('0.01'))
        stri = "{:<7}{:14}{:10}{:12}".format(self.number, self.article_type.name, str(self.cost.currency) + str(dec),
                                             SupplierOrderState.STATE_CHOICES_MEANING[self.state])
        return stri

    @staticmethod
    def prefix_field_names(model, prefix):
        fields = model._meta.get_fields()
        ret = []
        for field in fields:
            if not isinstance(field, ForeignObjectRel):
                ret.append(prefix + field.name)
        return ret

    @staticmethod
    def get_sol_combinations(supplier_order=None, article_type=None, state=None, qs=SupplierOrderLine.objects, include_price_field=True):
        # TODO: Add more fancyness like group by order
        result = []
        filtr = {}
        if supplier_order:
            filtr['supplier_order'] = supplier_order
        if article_type:
            filtr['article_type'] = article_type
        if state:
            filtr['state'] = state

        price_fields = []
        if include_price_field:
            price_fields = ['line_cost', 'line_cost_currency']

        flds = price_fields + SupplierOrderCombinationLine.prefix_field_names(ArticleType, 'article_type__')

        supplierorderlines = qs.filter(**filtr). \
            values('state', *flds).annotate(Count('id'))
        for o in supplierorderlines:
            number = o['id__count']
            state = o['state']
            if not include_price_field:
                amount = Decimal(-1)
                currency = Currency(iso=USED_CURRENCY)
            else:
                amount = o['line_cost']
                currency = o['line_cost_currency']
            cost = Cost(amount=amount, currency=currency)
            socl = SupplierOrderCombinationLine(number=number,
                                                article_type=ArticleType(name=o['article_type__name'],
                                                                         pk=o['article_type__id']),
                                                cost=cost,
                                                state=state)
            result.append(socl)
        return result


class DisbributionStrategy:

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
        :param distribution: A list of SupplierOrderLines
        :param indirect: Indirection flag. Function must be called indirectly.
        """
        assert isinstance(user, User)
        assert isinstance(supplier, Supplier)
        if not indirect:
            raise IndirectionError("Distribute must be called indirectly")
        assert distribution
        supplier_order = SupplierOrder(user_modified=user, supplier=supplier)
        for supplier_order_line in distribution:
            assert isinstance(supplier_order_line, SupplierOrderLine)
            assert supplier_order_line.order_line is None or isinstance(supplier_order_line.order_line, OrderLine)
            supplier_order_line.supplier_article_type = ArticleTypeSupplier.objects.get(article_type=supplier_order_line.article_type,
                                                                                        supplier=supplier)
            if supplier_order_line.order_line is not None:
                # Discount the possibility of OrProducts for now
                assert supplier_order_line.article_type == supplier_order_line.order_line.wishable.sellabletype.articletype

        # We've checked everyting, now we start saving
        supplier_order.save()
        for supplier_order_line in distribution:
            supplier_order_line.supplier_order = supplier_order
            supplier_order_line.user_modified = user
            supplier_order_line.save()

    @staticmethod
    def get_distribution(article_type_number_combos):
        """
        Proposes a distribution according to the specific strategy. Assume supply is not bigger than demand
        :param article_type_number_combos:
        :return: A list containing SupplierOrderLines
        """
        raise UnimplementedError("Super distribution class has no implementation")


class IndiscriminateCustomerStockStrategy(DisbributionStrategy):

    @staticmethod
    def get_distribution(article_type_number_combos):
        distribution = []
        articletype_dict = defaultdict(lambda: 0)
        for articletype, number, cost in article_type_number_combos:
            articletype_dict[articletype] += number
        articletypes = articletype_dict.keys()
        relevant_orderlines = OrderLine.objects.filter(state='O', wishable__in=articletypes).order_by('pk')
        # Match the orders one-by-one, stopping when all orders and wishes are fulfilled or article from the
        # article type number combos run out
        articletype_dict_supply = articletype_dict.copy()
        for orderline in relevant_orderlines:
            # Discount the possibility for OrProducts for now
            if hasattr(orderline.wishable, 'sellabletype') and hasattr(orderline.wishable.sellabletype, 'articletype'):
                if articletype_dict_supply[orderline.wishable.sellabletype.articletype] > 0:
                    sup_ord_line = SupplierOrderLine(article_type=orderline.wishable.sellabletype.articletype,
                                                     order_line=orderline, line_cost=None)
                    distribution.append(sup_ord_line)
                    articletype_dict_supply[orderline.wishable.sellabletype.articletype] -= 1
        stock_wishes = StockWishTableLine.objects.filter(article_type__in=articletypes)
        for wish in stock_wishes:
            assert wish.number >= articletype_dict_supply[wish.article_type]  # Assert not more supply than demand
            if articletype_dict_supply[wish.article_type] > 0:
                for i in range(0, articletype_dict_supply[wish.article_type]):
                    sup_ord_line = SupplierOrderLine(article_type=wish.article_type, line_cost=None)
                    distribution.append(sup_ord_line)
                articletype_dict_supply[wish.article_type] = 0

        # Now connect the cost. I do not think this can be done more efficiently.
        # Unfortunately, its n^2. This can be done more efficiently using maps, this should be worked out
        # sat a later date.
        cost_counter = article_type_number_combos.copy()
        for single_counter in cost_counter:
            ARTICLE_TYPE_LOCATION = 0
            ARTICLE_TYPE_NUMBER_LOCATION = 1
            ARTICLE_TYPE_COST_LOCATION = 2
            while single_counter[ARTICLE_TYPE_NUMBER_LOCATION] > 0:
                for supplier_order_line in distribution:
                    if supplier_order_line.article_type == single_counter[ARTICLE_TYPE_LOCATION] and \
                            (supplier_order_line.line_cost is None):
                        supplier_order_line.line_cost = single_counter[ARTICLE_TYPE_COST_LOCATION]
                        single_counter[ARTICLE_TYPE_NUMBER_LOCATION] -= 1
                        break

        return distribution


class UnimplementedError(Exception):
    pass


class CannotRemoveFromWishTableError(Exception):
    pass


class IndirectionError(Exception):
    pass


class InsufficientDemandError(Exception):
    pass


class ObjectNotSavedError(Exception):
    pass


class IncorrectStateError(Exception):
    pass


class IncorrectTransitionError(Exception):
    pass

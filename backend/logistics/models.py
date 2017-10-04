from collections import defaultdict
from decimal import Decimal

from django.db import models, transaction
from django.db.models import Count
from django.db.models.fields.reverse_related import ForeignObjectRel

from article.models import ArticleType, OrProductType
from blame.models import ImmutableBlame, Blame
from crm.models import User
from money.models import CostField, Cost, Currency
from order.models import OrderLine, OrderCombinationLine
from supplier.models import Supplier, ArticleTypeSupplier
from swipe.settings import USED_SUPPLIERORDER_STRATEGY, USED_CURRENCY
from tools.util import raiseif


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
        :param user_modified: user to which the order is authorized
        :param supplier: supplier which should order the products
        :param articles_ordered:
        :type articles_ordered: List[List[ArticleType, int, Cost]]
        :param allow_different_currency: If true, removes checks for the currency to see if its the system currency
        """

        ordered_dict = SupplierOrder.verify_data_assertions(user_modified, supplier, articles_ordered,
                                                            allow_different_currency)

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
        distribution = DistributionStrategy.get_strategy_from_string(USED_SUPPLIERORDER_STRATEGY)\
            .get_distribution(articles_ordered)

        DistributionStrategy.distribute(user_modified, supplier, distribution, indirect=True)

    @staticmethod
    def verify_article_demand(articles_ordered=None):
        """
        :param articles_ordered:
        :type articles_ordered: Dict[ArticleType, int]
        :return: List[Tuple[ArticleType, int]]
        """
        raiseif(articles_ordered is None,
                IncorrectDataError, "I must get articles that are ordered, I cannot check without")

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
            print("line:", line)
            print("line.wishable:", line.wishable)
            print("line.wishable.sellabletyoe:", line.wishable.sellabletype)
            print("line.wishable.sellabletype.articletype", line.wishable.sellabletype.articletype)
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
        :param articles_ordered
        :type articles_ordered: List[List[ArticleType, int]]
        :param allow_different_currency
        """
        raiseif(not user, IncorrectDataError, "You must supply me with a user which does this action")
        raiseif(not articles_ordered, IncorrectDataError, "You must supply me with articles that are being ordered")
        raiseif(not isinstance(user, User), IncorrectDataError, "user must be a User")

        # Ensure that the number of articles ordered is not less than 0

        ordered_dict = defaultdict(lambda: 0)

        for article, number, cost in articles_ordered:
            raiseif(not isinstance(article, ArticleType),
                    IncorrectDataError, "articles_ordered must be iterable of Tuple[ArticleType, int, Cost]")
            raiseif(not isinstance(number, int), IncorrectDataError,
                    "articles_ordered must be iterable of Tuple[ArticleType, int, Cost]")
            raiseif(not isinstance(cost, Cost), IncorrectDataError,
                    "articles_ordered must be iterable of Tuple[ArticleType, int, Cost]")

            if not allow_different_currency:
                raiseif(cost.currency.iso != USED_CURRENCY,
                        IncorrectDataError,
                        "You can only use currency {} with the current settings".format(USED_CURRENCY))
            raiseif(number <= 0, IncorrectDataError, "You cannot order negative amounts of products")
            ordered_dict[article] += number
            raiseif(not ArticleTypeSupplier.objects.get(article_type=article, supplier=supplier),
                    IncorrectDataError, "Article does not (yet) exist at supplier")
        return ordered_dict


class SupplierOrderLine(Blame):
    """
    Single ArticleType ordered at supplier and contained in a SupplierOrder. Can be linked to a Customers OrderLines or
    be left empty for stock.
    """
    # The document containing all these supplierOrderLines
    supplier_order = models.ForeignKey(SupplierOrder)
    # An articleType. Must match the supplierArticleType
    article_type = models.ForeignKey(ArticleType)
    # The articleType as the supplier knows it. Must match our own articleType
    supplier_article_type = models.ForeignKey(ArticleTypeSupplier)
    # An orderLine to fulfill the wish of a customer for a product. Null for stockwish(anonymously)
    order_line = models.ForeignKey(OrderLine, null=True)
    # The amount of money we are going to pay for this product excluding all taxes
    line_cost = CostField()
    # A state indicating if the customer order is completed yet.
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
                raiseif(
                    not ArticleType.objects.filter(
                        orproducttype__id=self.order_line.id,
                        id=self.article_type.id).exists(),
                    InvalidDataError, "Ordered article is not known to ordered OrProduct")
            else:
                # Customer article matches ordered article
                raiseif(not self.order_line.wishable.sellabletype.articletype == self.article_type,
                        InvalidDataError, "The order's article type is not this line's ArticleType")
            # +1 query for customer ordered lines
        checked_ats = False
        if not hasattr(self, 'supplier_article_type') or self.supplier_article_type is None:
            sup_art_types = ArticleTypeSupplier.objects.filter(
                article_type=self.article_type,
                supplier=self.supplier_order.supplier)
            # shouldn't get triggered, but +1 query
            checked_ats = True

            raiseif(len(sup_art_types) != 1, InvalidDataError, "There can only be one SupplierArticleType")

        if not checked_ats:  # should happen all the time
            raiseif(self.supplier_article_type.supplier != self.supplier_order.supplier,
                    InvalidDataError, "The supplier_order's supplier must be the supplier of the "
                                      "supplier_article_type")  # Article can be ordered at supplier
            # +2 query to get the supplier from the supplier_article_type and supplier_order
            raiseif(self.supplier_article_type != ArticleTypeSupplier.objects
                    .get(article_type=self.article_type,
                         supplier=self.supplier_order.supplier),
                    InvalidDataError, "The supplier_article_type must be ")  # optional +1 for article type

        # Set the relevant state is not implemented
        if self.pk is None:
            self.state = 'O'
        raiseif(self.state not in SupplierOrderState.STATE_CHOICES, InvalidDataError)
        # Assert that everything is ok here
        if self.pk is None:
            if self.order_line is not None:
                self.order_line.order_at_supplier(self.supplier_order.user_created)
                # ^ If this doesn't happen at exactly the same time
                # as the save of the SupOrdLn, you are screwed
            # +1 query for the user_created from supplier_order
            else:
                StockWishTable.remove_products_from_table(self.user_modified, article_type=self.article_type, number=1,
                                                          supplier_order=self.supplier_order, stock_wish=None,
                                                          indirect=True)
            # +1 query to remove one product from the stockwishtable, or to change the state of our order_line
            super(SupplierOrderLine, self).save(**kwargs)
            # +1 query to save the SOL itself
            sos = SupplierOrderState(supplier_order_line=self, state=self.state, user_modified=self.user_modified)
            sos.save()
            # +1 query to save the state transition
        else:
            # Maybe some extra logic here?
            super(SupplierOrderLine, self).save(**kwargs)

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
    @staticmethod
    def bulk_create_supplierorders(supplier_orderlines, supplier_order: SupplierOrder, user: User):
        """
        Creates supplierOrderLines in bulk with one transaction. This should not be called directly as it contains
        no checks for speed purposes. These checks are done in the main creation function so use that one for
        the creation of supplierOrderLines.
        :param supplier_orderlines:
        :type supplier_orderlines: list[SupplierOrderLine]
        :param supplier_order:
        :param user:
        :return:
        """
        sol_states = []
        ol_transitions = []  # type: list[OrderLine]
        remove_from_stock_wishes = defaultdict(lambda: 0)
        for sol in supplier_orderlines:
            sol.supplier_order = supplier_order
            sol.user_created = user
            sol.user_modified = user
            sol.state = 'O'
            # Explicitly do not check if the articleType matches the articleType of the OrderLine
            # Explicitly do not check if the supplierArticleType is set and matches the articleType
            # Explicity do not check if the supplier can supply the article
            if not sol.order_line:
                remove_from_stock_wishes[sol.article_type] += 1
            else:
                ol_transitions.append(sol.order_line)

        with transaction.atomic():
            for art in remove_from_stock_wishes:
                # Remove all products from table one by one
                StockWishTable.remove_products_from_table(user, article_type=art, number=remove_from_stock_wishes[art],
                                                          supplier_order=supplier_order, stock_wish=None,
                                                          indirect=True)
            SupplierOrderLine.objects.bulk_create(supplier_orderlines)
            sols_nw = SupplierOrderLine.objects.filter(supplier_order=supplier_order)
            for sol in sols_nw:
               sol_states.append(SupplierOrderState(supplier_order_line=sol, state=sol.state,
                                                         user_modified=user, user_created=user))
            SupplierOrderState.objects.bulk_create(sol_states)
            for ol in ol_transitions:
                ol.order_at_supplier(user)

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
    """
    A state log of a supplierOrderLine. The static lists indicate which states are available and
    what they mean. This also indicates which states are in transit and which are closed.
    """

    STATE_CHOICES = ('O', 'B', 'C', 'A')
    STATE_CHOICES_MEANING = {'O': 'Ordered at supplier', 'B': 'Backorder', 'C': 'Cancelled',
                             'A': 'Arrived at store'}
    OPEN_STATES = ('O', 'B')
    CLOSED_STATES = ('C', 'A')

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
        raiseif(user_modified is None, IncorrectDataError, "You must provide me with a user_modified")
        raiseif(len(articles_ordered) == 0, IncorrectDataError, "You must order at least 1 article to save")
        raiseif(not isinstance(user_modified, User), IncorrectDataError, "The user_modified argument must be a User")

        for article, number in articles_ordered:
            raiseif(not isinstance(article, ArticleType),
                    IncorrectDataError, "articles_ordered must be iterable of Tuple[ArticleType, int]")
            raiseif(not isinstance(number, int),
                    IncorrectDataError, "articles_ordered must be iterable of Tuple[ArticleType, int]")
            raiseif(number == 0, IncorrectDataError, "You may not order zero articles")

        stock_wish = StockWish(user_modified=user_modified)
        stock_wish.save()

        for article, number in articles_ordered:
            if number < 0:
                StockWishTable.remove_products_from_table(
                    user_modified,
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
        raiseif(not indirect,
                IndirectionError,
                "StockWishTableLine must be called indirectly from StockWishTable")

        super(StockWishTableLine, self).save(**kwargs)


class StockWishTable:
    """
    Helper methods for creating Stock Wishes. Let functions that modify the stock wish table call these functions
    """

    @staticmethod
    def add_products_to_table(user_modified, article_type, number, indirect=False,
                              stock_wish=None, supplier_order=None):
        raiseif(number <= 0, IncorrectDataError, "Number of products to add to table must be bigger than 0")

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
    def remove_products_from_table(user_modified, article_type, number, indirect=False,
                                   stock_wish=None, supplier_order=None):
        raiseif(number <= 0, IncorrectDataError, "number of products to remove from table must be bigger than 0")
        if not indirect:
            raise IndirectionError("remove_products_from_table must be called indirectly")
        article_type_statuses = StockWishTableLine.objects.filter(article_type=article_type)
        if not article_type_statuses:
            return
        article_type_status = article_type_statuses[0]
        if article_type_status.number - number < 0:
            raise CannotRemoveFromWishTableError("For articleType, tried to remove {} from WishTable,"
                                                 "but only {} is present".format(number, article_type_status.number))
        else:
            if article_type_status.number - number == 0:
                article_type_status.delete()
            else:
                article_type_status.number -= number
                article_type_status.save(indirect=indirect)

            log = StockWishTableLog(number=-number, article_type=article_type, stock_wish=stock_wish,
                                    supplier_order=supplier_order, user_modified=user_modified)
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
        raiseif(not indirect, IndirectionError, "Saving must be done indirectly")

        raiseif(self.supplier_order and self.stock_wish,
                TooManyReasonsError, "With two reasons to order this product, "
                                     "Choose either a supplier order or a stock wish")
        raiseif(not (self.supplier_order or self.stock_wish),
                NotEnoughReasonError, "Supply a reason for this modification")
        # ^ reason is either supplier order or stock wish modification
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
    """
    A helper class to group SupplierOrderLines together based on shared properties. This allows for quick summaries
    where summation of all lines was a bad alternative.
    """

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
        # noinspection PyProtectedMember
        fields = model._meta.get_fields()
        ret = []
        for field in fields:
            if not isinstance(field, ForeignObjectRel):
                ret.append(prefix + field.name)
        return ret

    @staticmethod
    def get_sol_combinations(supplier_order=None, article_type=None, state=None, qs=SupplierOrderLine.objects,
                             include_price_field=True, supplier=None):
        result = []
        filtr = {}
        if supplier_order:
            filtr['supplier_order'] = supplier_order
        if article_type:
            filtr['article_type'] = article_type
        if state:
            filtr['state'] = state
        if supplier:
            filtr['supplier_order__supplier'] = supplier
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
                currency = Currency(iso=o['line_cost_currency'])
            cost = Cost(amount=amount, currency=currency)
            socl = SupplierOrderCombinationLine(number=number,
                                                article_type=ArticleType(name=o['article_type__name'],
                                                                         pk=o['article_type__id']),
                                                cost=cost,
                                                state=state)
            result.append(socl)
        return result


class DistributionStrategy:
    """
    An interface for a consistent way of deciding the distribution of the products ordered at our suppliers. Also
    contains a distributionfunction that actually handles the actual distribution of the articles for users who
    prefer a manual way of operation.
    """

    @staticmethod
    def get_strategy_from_string(strategy):
        if strategy == "IndiscriminateCustomerStockStrategy":
            return IndiscriminateCustomerStockStrategy
        else:
            raise UnimplementedError("Strategy not implemented")

    @staticmethod
    def distribute(user, supplier, distribution, indirect=False):
        """
        Creates the supplier order and distributes the SupplierOrderLines to any orders
        :param user: a User for the SupplierOrder
        :param supplier: Supplier for the SupplierOrder
        :param distribution: A list of SupplierOrderLines
        :param indirect: Indirection flag. Function must be called indirectly.
        """
        raiseif(not isinstance(user, User), IncorrectDataError, "argument user is not instance of User")
        raiseif(not isinstance(supplier, Supplier), IncorrectDataError, "argument supplier is not instance of Supplier")
        raiseif(not indirect, IndirectionError, "Distribute must be called indirectly")
        raiseif(not distribution, IncorrectDataError, "distribution is not supplied")

        supplier_order = SupplierOrder(user_modified=user, supplier=supplier)
        articles = set()
        article_type_suppliers = {}

        for supplier_order_line in distribution:
            raiseif(
                not isinstance(supplier_order_line, SupplierOrderLine),
                IncorrectDataError, "argument distribution does not only contain SupplierOrderLine")
            raiseif(not (supplier_order_line.order_line is None or
                         isinstance(supplier_order_line.order_line, OrderLine)),
                    IncorrectDataError, "supplier order line's order line link is not instance of OrderLine")

            articles.add(supplier_order_line.article_type)
            if supplier_order_line.order_line is not None:
                # Discount the possibility of OrProducts for now
                raiseif(supplier_order_line.article_type_id !=
                        supplier_order_line.order_line.wishable_id,
                        IncorrectDataError, "SupplierOrderLine's article type is not the same type as it's linked"
                                            "OrderLine")
        art_sup_types = ArticleTypeSupplier.objects.filter(article_type__in=articles, supplier=supplier)
        for ats in art_sup_types:
            article_type_suppliers[ats.article_type] = ats

        # Add articleTypeSuppliers all at once
        for supplier_order_line in distribution:
            ats = article_type_suppliers.get(supplier_order_line.article_type)
            if ats is None:
                raise IncorrectDataError("Article {} does not "
                                         "have an ArticleTypeSupplier".format(supplier_order_line.article_type))
            supplier_order_line.supplier_article_type = ats

        # We've checked everyting, now we start saving
        with transaction.atomic():
            supplier_order.save()
            SupplierOrderLine.bulk_create_supplierorders(distribution, supplier_order, user)

    @staticmethod
    def get_distribution(article_type_number_combos):
        """
        Proposes a distribution according to the specific strategy. Assume supply is not bigger than demand
        :param article_type_number_combos: List[ArticleType, number, Cost]
        :return: A list containing SupplierOrderLines
        """
        raise UnimplementedError("Super distribution class has no implementation")


class IndiscriminateCustomerStockStrategy(DistributionStrategy):
    """
    Prioritises the customers first by primary key of orderline, and then the stock.
    """

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
            # Assert not more supply than demand
            raiseif(wish.number < articletype_dict_supply[wish.article_type],
                    InsufficientDemandError, "there is not enough demand to order this many articles")

            if articletype_dict_supply[wish.article_type] > 0:
                for i in range(0, articletype_dict_supply[wish.article_type]):
                    sup_ord_line = SupplierOrderLine(article_type=wish.article_type, line_cost=None)
                    distribution.append(sup_ord_line)
                articletype_dict_supply[wish.article_type] = 0

        # Now connect the cost.
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
    """
    Used for still unimplemented features in the logistics scope.
    """
    pass


class CannotRemoveFromWishTableError(Exception):
    """
    The system tries to remove more from the WishTable than there is present. This is not consistent.
    """
    pass


class IndirectionError(Exception):
    """
    Thrown when a function is abusively used in an indirect manner(indirect-flag).
    """
    pass


class InsufficientDemandError(Exception):
    """
    There is more supply than demand.
    """
    pass


class ObjectNotSavedError(Exception):
    """
    A transition is attempted on an unsaved object.
    """
    pass


class IncorrectStateError(Exception):
    """
    An incorrect state is supplied.
    """
    pass


class IncorrectTransitionError(Exception):
    """
    An illegal transition is attempted.
    """
    pass


class IncorrectDataError(Exception):
    """
    Data is supplied in an incorrect manner or type.
    """
    pass


class TooManyReasonsError(Exception):
    """
    Two reasons were supplied for modifying the wishTable.
    """
    pass


class NotEnoughReasonError(Exception):
    """
    No reason was supplied for modifying the wishTable.
    """
    pass


class InvalidDataError(Exception):
    """
    Data is supplied that, after further inspection, does not meet the specified criteria.
    """
    pass

from collections import defaultdict

from django.db import models, transaction

from article.models import ArticleType
from blame.models import ImmutableBlame, Blame
from crm.models import User
from logistics.models import SupplierOrderLine, SupplierOrderCombinationLine, \
    InsufficientDemandError, IndirectionError, UnimplementedError, SupplierOrderState
from money.models import CostField, Cost
from stock.enumeration import enum
from stock.models import StockChangeSet
from stock.stocklabel import OrderLabel
from supplier.models import Supplier, ArticleTypeSupplier
from swipe.settings import USED_SUPPLICATION_STRATEGY
from tools.util import raiseif


class PackingDocument(ImmutableBlame):
    # The supplier that supplies the ArticleTypes
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    # The identifier for the document. This is not neccesarily unique, but it should match real packing documents.
    supplier_identifier = models.CharField(max_length=30)

    @staticmethod
    @transaction.atomic
    def create_packing_document(user, supplier, packing_document_name,
                                article_type_cost_combinations, invoice_name=None, serial_numbers=None):
        """
        Creates a packing document from the supplied information. This registers that the products have arrived
        at the store. It is linked to a single supplier, since that is the way you process packing documents.
        :param user: Blamed user
        :param supplier: Supplier for this packing document
        :param packing_document_name: Name of the packing document. Obligatory
        :param article_type_cost_combinations: A list containing lists containing a combination of an ArticleType,
                a number of those ArticleTypes, and potentially a cost if provided by an invoice.
        :type article_type_cost_combinations: list[tuple[ArticleType, number, [Cost]]]
        :param invoice_name: Name of an invoice. If None, no invoice is to be expected
        :param serial_numbers: A list of serial number strings packed together by article
        :type serial_numbers: dict(articleType,list[SerialNumberStrings])
        :return:
        """
        use_invoice = False
        if invoice_name is not None:
            use_invoice = True
            raiseif(not isinstance(invoice_name, str), InvalidDataError, "Invoice name must be string")
        raiseif(not isinstance(user, User), InvalidDataError, "user must be a User")
        raiseif(not isinstance(supplier, Supplier), InvalidDataError, "supplier must be a Supplier")
        raiseif(not isinstance(packing_document_name, str), InvalidDataError, "packing document name must be a string")
        raiseif(not isinstance(article_type_cost_combinations, list), InvalidDataError, "a28s must be a list")

        ARTICLETYPE_LOCATION = 0
        NUMBER_LOCATION = 1
        COST_LOCATION = 2
        for atcc in article_type_cost_combinations:
            raiseif(not isinstance(atcc[ARTICLETYPE_LOCATION], ArticleType), InvalidDataError,
                    "a28s[n] is not an ArticleType")
            raiseif(not isinstance(atcc[NUMBER_LOCATION], int), InvalidDataError, "a28s[n] is not a number")
            if use_invoice:
                raiseif(len(atcc) != 2 and atcc[COST_LOCATION] is not None and
                        not isinstance(atcc[COST_LOCATION], Cost), InvalidDataError, "a28s[n] is not a Cost")
            else:
                raiseif(len(atcc) != 2 and atcc[COST_LOCATION] is not None, InvalidDataError, "a28s[n] is not None")

        errors = PackingDocument.verify_article_demand(supplier, article_type_cost_combinations, use_invoice)
        if len(errors) > 0:
            err_msg = "Not enough demand for ordered articles: \n"
            for article, number in errors:
                err_msg += \
                    " - Article {article} was ordered {number} times too many".format(
                        article=article.name,
                        number=number
                    )
                err_msg += "\n"
            raise InsufficientDemandError(err_msg)

        if serial_numbers:
            PackingDocument.verify_serial_numbers(article_type_cost_combinations, serial_numbers)

        distribution_strategy = DistributionStrategy.get_strategy_from_string(USED_SUPPLICATION_STRATEGY)
        distribution = distribution_strategy.get_distribution(supplier=supplier,
                                                              article_type_number_combos=article_type_cost_combinations)
        changeset = DistributionStrategy.build_changeset(distribution)

        DistributionStrategy.distribute(user=user, supplier=supplier,
                                        distribution=distribution,
                                        document_identifier=packing_document_name,
                                        invoice_identifier=invoice_name,
                                        mod_stock=False,
                                        serial_numbers=serial_numbers,
                                        indirect=True
                                        )
        pd = PackingDocument.objects.last()
        StockChangeSet.construct("Stock supplication by {}".format(pd.pk), entries=changeset, enum=enum["supplication"])

    @staticmethod
    def verify_article_demand(supplier, article_type_cost_combinations=None, use_invoice=True):
        raiseif(not article_type_cost_combinations and not isinstance(article_type_cost_combinations, list),
                InvalidDataError, )

        supplier_ordered_articles = defaultdict(lambda: 0)
        socls = SupplierOrderCombinationLine.get_sol_combinations(state='O', supplier=supplier)
        for socl in socls:
            supplier_ordered_articles[socl.article_type] += socl.number
        supplied_articles = defaultdict(lambda: 0)
        for atcc in article_type_cost_combinations:
            raiseif(not isinstance(atcc[0], ArticleType),
                    InvalidDataError, "attc[n] must be Tuple[ArticleType, integer]")
            raiseif(not isinstance(atcc[1], int),
                    InvalidDataError, "attc[n] must be Tuple[ArticleType, integer]")
            if not use_invoice:
                raiseif(len(atcc) != 2, InvalidDataError, "attc[n] must be a Tuple[ArticleType, integer]")
            else:
                raiseif(len(atcc) != 2 and atcc[2] is not None and not isinstance(atcc[2], Cost),
                        InvalidDataError, "attc[n] must be a Tuple[ArticleType, integer]")
            supplied_articles[atcc[0]] += atcc[1]

        errors = []
        for article in supplied_articles:
            if supplied_articles[article] > supplier_ordered_articles[article]:
                errors.append((article, supplied_articles[article] - supplier_ordered_articles[article]))
        return errors

    @staticmethod
    def verify_serial_numbers(article_type_cost_combinations, serial_numbers):
        ARTICLETYPE_LOCATION = 0
        NUMBER_LOCATION = 1
        article_type_counter = defaultdict(lambda: 0)
        for atcc in article_type_cost_combinations:
            article_type_counter[atcc[ARTICLETYPE_LOCATION]] += atcc[NUMBER_LOCATION]
        for article in serial_numbers:
            if len(serial_numbers[article]) > article_type_counter.get(article, 0):
                raise IncorrectDataError("More serial number for articleType {} "
                                         "than there are articles in the packing document".format(article.name))


class SerialNumber(models.Model):
    """
    Since individual products are not registered, when they enter the system they do so as a group of products and then
    they move to stock. In order to still facilitate serial numbers, they are registered in the only place logical to
    the system, that is the packing document.
    """
    # The serial number itself
    identifier = models.CharField(max_length=255)
    # The articleType to which the serial number is connected
    article_type = models.ForeignKey(ArticleType)
    # The packing document where the serial number is registered
    packing_document = models.ForeignKey(PackingDocument)

    def __str__(self):
        if not hasattr(self, 'article_type') or self.article_type is None:
            at = "None"
        else:
            at = self.article_type
        if not hasattr(self, 'packing_document') or self.packing_document is None:
            pd = "None"
        else:
            pd = self.packing_document.id
        return "Identifier: {}, ArticleType: {}, Packing Document: {}".format(self.identifier, at, pd)


class Invoice(ImmutableBlame):
    """
    An invoice for products delivered. Supplied after a packing document and not essential to the process. Can technically
    used to correct errors made by the person ordering the products and setting the prices.
    """
    # The supplier name for the invoice
    supplier_identifier = models.CharField(max_length=30)
    # The supplier of the packing document and products of this invoice
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)


class PackingDocumentLine(Blame):
    """
    An important part of the logistical process. This document line indicates that products have arrived from the supplier.
    When these are saved, the stock is modified based on the SupplierOrderLines that are connected to the packingdocumentlines.
    The step of saving shifts the orders of customers as a result of the connection a SupplierOrderLine. Semi-final prices
    are assumed for the products that enter stock.
    """
    # The packing document to which this line belongs
    packing_document = models.ForeignKey(PackingDocument, on_delete=models.PROTECT)
    # The line which will match this line
    supplier_order_line = models.ForeignKey(SupplierOrderLine, on_delete=models.PROTECT)
    # The article type
    article_type = models.ForeignKey(ArticleType)
    # The cost from the supplierOrderLine
    line_cost = CostField()
    # Final cost after retrieving it from the Invoice
    line_cost_after_invoice = CostField(null=True, default=None)
    # Link to the invoice if available
    invoice = models.ForeignKey(Invoice, null=True, on_delete=models.PROTECT)

    @transaction.atomic
    def save(self, mod_stock=True):
        """
        Save function for a packing document line. Modifies related supplier orders.
        WARNING: Modifies stock depending on flag.
        :param mod_stock: Indicated whether saving this PacDocLine also mods the stock. If not,
        this has to be done manually
        :return:
        """
        raiseif(not self.packing_document, InvalidDataError, "You must have an packing document")
        raiseif(not isinstance(self.packing_document, PackingDocument),
                InvalidDataError, "packing document must be a PackingDocument")
        raiseif(not self.supplier_order_line, InvalidDataError, "You must specify supplier_order_line")
        raiseif(not isinstance(self.supplier_order_line, SupplierOrderLine),
                InvalidDataError, "supplier_order_line must be a SupplierOrderLine")
        if self.line_cost is not None:
            raiseif(not isinstance(self.line_cost, Cost), InvalidDataError, "line_cost must be a Cost")

        # All assertions done, now we check the cost
        # Line_cost_after_invoice should be connected to an invoice. Therefore, we cannot have an invoice
        # without the other
        if hasattr(self, 'invoice') and self.invoice is not None:
            raiseif(self.line_cost_after_invoice is None,
                    InvalidDataError, "line_cost_after_invoice must be present if invoice is present")

        # Retrieve Cost from SupplierOrderLine
        self.line_cost = self.supplier_order_line.line_cost

        raiseif(not self.article_type, InvalidDataError, "must specify article_type")
        raiseif(not isinstance(self.article_type, ArticleType), InvalidDataError, "article_type is not an ArticleType")
        raiseif(self.article_type != self.supplier_order_line.article_type,
                IncorrectDataError, "article should be the same for this and supplier_order_line ")

        raiseif(not ArticleTypeSupplier.objects.get(supplier=self.packing_document.supplier,
                                                    article_type=self.article_type),
                NoValidSupplierError, "This product is not available in the given supplier's assortment")

        # All checks are done, now we save everyting
        # Mod supplierOrderLine and order if connected and packingdoc is new
        if self.pk is None:
            self.supplier_order_line.mark_as_arrived(self.packing_document.user_created)
            document_key = self.packing_document.pk

            super(PackingDocumentLine, self).save()
            if mod_stock:
                # Modify stock
                entry = [{
                    'article': self.supplier_order_line.article_type,
                    'book_value': self.line_cost,
                    'count': 1,
                    'is_in': True
                }]
                if hasattr(self.supplier_order_line, 'order_line') and self.supplier_order_line.order_line is not None:
                    label = OrderLabel(self.supplier_order_line.order_line.order.pk)
                    entry[0]['label'] = label
                StockChangeSet.construct(description="Stock supplication by {}".format(document_key), entries=entry,
                                         enum=enum["supplication"])
        else:
            super(PackingDocumentLine, self).save()

    def __str__(self):
        if not hasattr(self, 'line_cost'):
            cost = "None"
        else:
            cost = str(self.line_cost)
        if not hasattr(self, 'invoice') or self.invoice is None:
            invoice = "None"
        else:
            invoice = self.invoice.pk
        if not hasattr(self, 'line_cost_after_invoice') or self.line_cost_after_invoice is None:
            final_cost = "None"
        else:
            final_cost = str(self.line_cost_after_invoice)
        if not hasattr(self, 'packing_document') or self.packing_document is None:
            packing_doc = "None"
        else:
            packing_doc = self.packing_document.pk
        if not hasattr(self, 'supplier_order_line') or self.supplier_order_line is None:
            sol = "None"
        else:
            sol = self.supplier_order_line.pk
        return "Packing Document: {}, SupplierOrderLine: {}, ArticleType: {}, SupOrdCost: {}, InvoiceCost: {}, " \
               "Invoice: {}".format(packing_doc, sol, self.article_type, cost, final_cost, invoice)


class DistributionStrategy:
    """
    The interface for strategies for distributing the arrived products. DistributionStrategy allows for a standardised
    way of asking for a way of distribution and there is also a function to handle the actual act of distribution.
    """

    @staticmethod
    @transaction.atomic
    def distribute(user, supplier, distribution, document_identifier, invoice_identifier=False, serial_numbers=None,
                   indirect=False, mod_stock=True):
        """
        Distributes the actual packing document. A line_cost_after invoice should never be used if there is not direct
        invoice possible, indicated by the invoice_identifier. Distribution will refuse to execute in this case.
        :param user: The user that caused this distribution
        :param supplier: The supplier that ships the products
        :param distribution: List[PackingDocumentLine], with each PackingDocumentLine
        :param document_identifier: String, name of the packing document
        :param invoice_identifier: String, can be empty if there is no invoice
        :param serial_numbers
        :param indirect: Indirection flag. Function is only meant to be called indirectly. Change at your own peril.
        :param mod_stock: Indicates whether the function actually
        :return:
        """
        if not indirect:
            raise IndirectionError("Distribute must be called indirectly")

        raiseif(not (user and isinstance(user, User)), IncorrectDataError, "user is not of type User")
        raiseif(not (supplier and isinstance(supplier, Supplier)), IncorrectDataError, "")
        raiseif(not (distribution and isinstance(distribution, list)), IncorrectDataError)
        raiseif(not (document_identifier and isinstance(document_identifier, str)), IncorrectDataError)
        # Indicates that we are using an invoice in the process
        if invoice_identifier:
            raiseif(not isinstance(invoice_identifier, str), IncorrectDataError)

        found_final_cost = False
        for pac_doc_line in distribution:
            raiseif(not pac_doc_line and not isinstance(pac_doc_line, PackingDocumentLine),
                    InvalidDataError, )
            # Asserts correct article type and supplier consistency
            raiseif(not pac_doc_line.supplier_order_line,
                    InvalidDataError, "pac_doc_line must have an supplier_order_line")
            raiseif(pac_doc_line.article_type != pac_doc_line.supplier_order_line.article_type, IncorrectDataError,
                    "Article types are not matching")
            raiseif(supplier != pac_doc_line.supplier_order_line.supplier_order.supplier, IncorrectDataError,
                    "suppliers are not matching")
            # There cannot be a final cost without an invoice
            if not invoice_identifier:
                raiseif(hasattr(pac_doc_line, 'line_cost_after_invoice') and pac_doc_line.line_cost_after_invoice,
                        InvalidDataError, "You must not have a line_cost_after_invoice if you ")
            if hasattr(pac_doc_line, 'line_cost_after_invoice') and pac_doc_line.line_cost_after_invoice is not None:
                found_final_cost = True

        invoice = None
        if invoice_identifier:
            # Checks if there is an actual final_line_cost for a pac_doc_line to create an invoice for
            raiseif(not found_final_cost, IncorrectDataError, "The invoice specified does not have this one's cost")
            invoice = Invoice(supplier=supplier, supplier_identifier=invoice_identifier, user_modified=user)

        serial_number_list = []
        if serial_numbers:
            for article_type in serial_numbers:
                for ser in serial_numbers[article_type]:
                    serial_number_list.append(SerialNumber(identifier=ser, article_type=article_type))

        # Below here are the actual saves
        # First, saves of related documents
        packing_document = PackingDocument(supplier=supplier, supplier_identifier=document_identifier,
                                           user_modified=user)
        packing_document.save()
        if invoice_identifier:
            invoice.save()
        if serial_numbers:
            for sn in serial_number_list:
                sn.packing_document = packing_document
                sn.save()
        # Saves and final parameter settings of packing document lines
        for pac_doc_line in distribution:
            pac_doc_line.packing_document = packing_document
            if hasattr(pac_doc_line, 'line_cost_after_invoice') and pac_doc_line.line_cost_after_invoice:
                pac_doc_line.invoice = invoice
            pac_doc_line.user_modified = user
            pac_doc_line.save(mod_stock=mod_stock)

    @staticmethod
    def get_distribution(article_type_number_combos, supplier):
        """
        Creates a distribution
        :param article_type_number_combos: List[ArticleType, number, [Cost]]. A list containing articletypes, a
        multiplicity of those article types, and a cost if the packing document line is connected to an invoice.
        :param supplier
        """
        raise UnimplementedError("Function does not exist at the super level. Call actual strategies")

    @staticmethod
    def get_strategy_from_string(strategy_name):
        if strategy_name == "FirstSupplierOrderStrategy":
            return FirstSupplierOrderStrategy
        elif strategy_name == "FirstCustomersDateTimeThenStockDateTime":
            return FirstCustomersDateTimeThenStockDateTime
        else:
            raise UnimplementedError("Strategy not implemented")

    @staticmethod
    def build_changeset(distribution):
        """
        Builds a changeset for the storage of the articles from the packing document lines
        :param distribution: List[PackingDocumentLine] containing fully complete packingDocLines
        ready for saving
        :return: A StockChangeSet with the necessary storages
        """
        raiseif(not distribution or not isinstance(distribution, list), InvalidDataError, "distribution is not a list")
        for pac_doc_line in distribution:
            raiseif(not isinstance(pac_doc_line, PackingDocumentLine),
                    InvalidDataError, "distribution does contain non-PackingDocumentLine s")
        # Creates a dictionary of dictionaries. The first layer comprises the Order pk's with 0 articles for stock.
        # The second layer is an articleType with a multiplicity and cost

        order_summary = {}
        for pac_doc_line in distribution:
            if pac_doc_line.supplier_order_line.order_line is not None:
                pk = pac_doc_line.supplier_order_line.order_line.order.pk
                result = order_summary.get(pk)
                if result is None:
                    order_summary[pk] = {}
                result2 = order_summary[pk].get((pac_doc_line.article_type, pac_doc_line.line_cost))
                if result2 is None:
                    order_summary[pk][(pac_doc_line.article_type, pac_doc_line.line_cost)] = 1
                else:
                    order_summary[pk][(pac_doc_line.article_type, pac_doc_line.line_cost)] += 1

            else:
                result = order_summary.get(0)
                if result is None:
                    order_summary[0] = {}
                result2 = order_summary[0].get((pac_doc_line.article_type, pac_doc_line.line_cost))
                if result2 is None:
                    order_summary[0][(pac_doc_line.article_type, pac_doc_line.line_cost)] = 1
                else:
                    order_summary[0][(pac_doc_line.article_type, pac_doc_line.line_cost)] += 1
        ARTICLE_TYPE_LOCATION = 0
        COST_LOCATION = 1

        stock_change_set = []
        for key in order_summary:
            if key == 0:
                for atcc in order_summary[0]:
                    stock_change_set.append({
                        'article': atcc[ARTICLE_TYPE_LOCATION],
                        'book_value': atcc[COST_LOCATION],
                        'count': order_summary[key][atcc],
                        'is_in': True,
                    })
            else:
                for atcc in order_summary[key]:
                    stock_change_set.append({
                        'article': atcc[0],
                        'book_value': atcc[1],
                        'count': order_summary[key][atcc],
                        'is_in': True,
                        'label': OrderLabel(key)
                    })
        return stock_change_set


class FirstSupplierOrderStrategy(DistributionStrategy):
    """
    A simple distribution strategy that uses the implied strategy used when prioritizing the SupplierOrders.
    """

    @staticmethod
    def get_distribution(article_type_number_combos, supplier):
        distribution = []
        # Viability assertions
        raiseif(not isinstance(supplier, Supplier), InvalidDataError, "supplier is not a Supplier")
        articletype_dict = defaultdict(lambda: 0)
        use_cost = False  # Indicates that invoice, provided costs are used
        ARTICLE_TYPE_LOCATION = 0
        NUMBER_LOCATION = 1
        COST_LOCATION = 2
        for elem in article_type_number_combos:
            articletype_dict[elem[0]] += elem[1]
            if len(elem) > 2 and elem[2] is not None and isinstance(elem[2], Cost):
                use_cost = True
        articletypes = articletype_dict.keys()
        relevant_supplier_orderline = SupplierOrderLine.objects.filter(state__in=SupplierOrderState.OPEN_STATES,
                                                                       article_type__in=articletypes,
                                                                       supplier_order__supplier=supplier)
        article_demand = defaultdict(lambda: 0)
        article_supply = articletype_dict.copy()

        # Tallies the open supplier orders
        for sol in relevant_supplier_orderline:
            article_demand[sol.article_type] += 1

        # If you have supply without demand, there is an inconsistency
        for typ in articletypes:
            raiseif(articletype_dict[typ] > article_demand[typ],
                    IncorrectDataError, "Amount ordered may not be more than there is demand")
        # Create the packing_document_lines
        for sol in relevant_supplier_orderline:
            if article_supply[sol.article_type] > 0:
                pac_doc_line = PackingDocumentLine(article_type=sol.article_type,
                                                   line_cost=sol.line_cost,
                                                   supplier_order_line=sol)
                distribution.append(pac_doc_line)
                article_supply[sol.article_type] -= 1

        # Should we consider costs? If true, connect cost to packing_doc_lines
        if use_cost:
            cost_dist = article_type_number_combos.copy()
            for pac_doc_line in distribution:
                for elem in cost_dist:
                    if pac_doc_line.article_type == elem[ARTICLE_TYPE_LOCATION] and elem[NUMBER_LOCATION] > 0 \
                            and len(elem) > 2 and elem[COST_LOCATION] is not None:
                        pac_doc_line.line_cost_after_invoice = elem[COST_LOCATION]
                        elem[NUMBER_LOCATION] -= 1
                        # Go to next packing doc line
                        break

        return distribution


class FirstCustomersDateTimeThenStockDateTime(DistributionStrategy):
    """
    Prioritizes the customers first by checking the supplier orders by date time. After that, the stock is supplied
    by datetime.
    """

    @staticmethod
    def get_distribution(article_type_number_combos, supplier):
        distribution = []
        # Viability assertions
        raiseif(not isinstance(supplier, Supplier), InvalidDataError, "supplier is not a Supplier")
        articletype_dict = defaultdict(lambda: 0)
        use_cost = False  # Indicates that invoice, provided costs are used
        ARTICLE_TYPE_LOCATION = 0
        NUMBER_LOCATION = 1
        COST_LOCATION = 2
        for elem in article_type_number_combos:
            articletype_dict[elem[0]] += elem[1]
            if len(elem) > 2 and elem[2] is not None and isinstance(elem[2], Cost):
                use_cost = True
        articletypes = articletype_dict.keys()
        relevant_supplier_orderline = SupplierOrderLine.objects.filter(state__in=SupplierOrderState.OPEN_STATES,
                                                                       article_type__in=articletypes,
                                                                       supplier_order__supplier=supplier)
        article_demand = defaultdict(lambda: 0)
        article_supply = articletype_dict.copy()

        # Tallies the open supplier orders
        for sol in relevant_supplier_orderline:
            article_demand[sol.article_type] += 1

        # If you have supply without demand, there is an inconsistency
        for typ in articletypes:
            raiseif(articletype_dict[typ] > article_demand[typ],
                    IncorrectDataError, "You cannot order more than there is demand")

        relevant_supplier_orderline_orders_only = SupplierOrderLine.objects.filter(state__in=SupplierOrderState.OPEN_STATES,
                                                                                   article_type__in=articletypes,
                                                                                   supplier_order__supplier=supplier,
                                                                                   order_line__isnull=False)
        # Create the packing_document_lines for orders
        for sol in relevant_supplier_orderline_orders_only:
            if article_supply[sol.article_type] > 0:
                pac_doc_line = PackingDocumentLine(article_type=sol.article_type,
                                                   line_cost=sol.line_cost
                                                   , supplier_order_line=sol)
                distribution.append(pac_doc_line)
                article_supply[sol.article_type] -= 1

        relevant_supplier_orderline_stock_only = SupplierOrderLine.objects.filter(state__in=SupplierOrderState.OPEN_STATES,
                                                                                  article_type__in=articletypes,
                                                                                  supplier_order__supplier=supplier,
                                                                                  order_line__isnull=True)

        # Create the packing_document_lines
        for sol in relevant_supplier_orderline_stock_only:
            if article_supply[sol.article_type] > 0:
                pac_doc_line = PackingDocumentLine(article_type=sol.article_type,
                                                   supplier_order_line=sol,
                                                   line_cost=sol.line_cost)
                distribution.append(pac_doc_line)
                article_supply[sol.article_type] -= 1

        # Should we consider costs? If true, connect cost to packing_doc_lines
        if use_cost:
            cost_dist = article_type_number_combos.copy()
            for pac_doc_line in distribution:
                for elem in cost_dist:
                    if pac_doc_line.article_type == elem[ARTICLE_TYPE_LOCATION] and elem[NUMBER_LOCATION] > 0 \
                            and len(elem) > 2 and elem[COST_LOCATION] is not None:
                        pac_doc_line.line_cost_after_invoice = elem[COST_LOCATION]
                        elem[NUMBER_LOCATION] -= 1
                        # Go to next packing doc line
                        break

        return distribution


class InvalidDataError(Exception):
    """
    If the data given is not of a valid type
    """
    pass


class IncorrectDataError(Exception):
    """
    If the data given does not have a valid value
    """
    pass


class NoValidSupplierError(Exception):
    """
    If the supplier is invalid
    """
    pass

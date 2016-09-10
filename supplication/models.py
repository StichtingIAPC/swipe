from django.db import models, transaction
from crm.models import User
from stock.enumeration import enum
from supplier.models import Supplier, ArticleTypeSupplier
from logistics.models import SupplierOrderLine, SupplierOrderCombinationLine, \
    InsufficientDemandError, IndirectionError, UnimplementedError, SupplierOrderState
from money.models import CostField, Cost
from stock.models import StockChangeSet
from stock.stocklabel import OrderLabel
from article.models import ArticleType
from blame.models import ImmutableBlame, Blame
from collections import defaultdict


class PackingDocument(ImmutableBlame):

    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)

    supplier_identifier = models.CharField(max_length=30)

    @staticmethod
    @transaction.atomic
    def create_packing_document(user, supplier, packing_document_name, article_type_cost_combinations, invoice_name=None):
        """
        Creates a packing document from the supplied information. This registers that the products have arrived at the store.
        It is linked to a single supplier, since that is the way you process packing documents.
        :param user: Blamed user
        :param supplier: Supplier for this packing document
        :param packing_document_name: Name of the packing document. Obligatory
        :param article_type_cost_combinations: List[List[ArticleType number [Cost]]]. A list containing lists containing
        A combination of an ArticleType, a number of those ArticleTypes, and potentially a cost if provided by an invoice.
        :param invoice_name: Name of an invoice. If None, no invoice is to be expected
        :return:
        """
        use_invoice = False
        if invoice_name is not None:
            use_invoice = True
            assert isinstance(invoice_name, str)
        assert isinstance(user, User)
        assert isinstance(supplier, Supplier)
        assert isinstance(packing_document_name, str)
        assert isinstance(article_type_cost_combinations, list)

        ARTICLETYPE_LOCATION = 0
        COST_LOCATION = 1
        for atcc in article_type_cost_combinations:
            assert isinstance(atcc[ARTICLETYPE_LOCATION], ArticleType)
            if use_invoice:
                assert atcc[COST_LOCATION] is None or isinstance(atcc[COST_LOCATION], Cost)
            else:
                assert atcc[COST_LOCATION] is None

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

    @staticmethod
    def verify_article_demand(supplier, article_type_cost_combinations=None, use_invoice=True):
        assert article_type_cost_combinations and isinstance(article_type_cost_combinations, list)

        supplier_ordered_articles = defaultdict(lambda: 0)
        socls = SupplierOrderCombinationLine.get_sol_combinations(state='O', supplier=supplier)
        for socl in socls:
            supplier_ordered_articles[socl.article_type] += socl.number
        supplied_articles = defaultdict(lambda: 0)
        for atcc in article_type_cost_combinations:
            assert isinstance(atcc[0], ArticleType)
            assert isinstance(atcc[1], int)
            if not use_invoice:
                assert atcc[2] is None
            else:
                assert atcc[2] is None or isinstance(atcc[2], Cost)
            supplied_articles[atcc[0]] += supplier_ordered_articles[atcc[1]]

        errors = []
        for article in supplied_articles:
            assert supplied_articles[article] <= supplier_ordered_articles[article]
            if supplied_articles[article] > supplier_ordered_articles[article]:
                errors.append((article, supplied_articles[article] - supplier_ordered_articles[article]))

        return errors


class Invoice(ImmutableBlame):

    supplier_identifier = models.CharField(max_length=30)

    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)


class PackingDocumentLine(Blame):
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
        assert self.packing_document
        assert isinstance(self.packing_document, PackingDocument)
        assert self.supplier_order_line
        assert isinstance(self.supplier_order_line, SupplierOrderLine)
        if self.line_cost is not None:
            assert isinstance(self.line_cost, Cost)

        # All assertions done, now we check the cost
        # Line_cost_after_invoice should be connected to an invoice. Therefore, we cannot have an invoice
        # without the other
        if hasattr(self, 'invoice') and self.invoice is not None:
            assert self.line_cost_after_invoice is not None

        # Retrieve Cost from SupplierOrderLine
        self.line_cost = self.supplier_order_line.line_cost

        assert self.article_type
        assert isinstance(self.article_type, ArticleType)
        assert self.article_type == self.supplier_order_line.article_type

        assert ArticleTypeSupplier.objects.get(supplier=self.packing_document.supplier, article_type=self.article_type)

        # All checks are done, now we save everyting
        # Mod supplierOrderLine and order if connected and packingdoc is new
        if self.pk is None:
            self.supplier_order_line.mark_as_arrived(self.packing_document.user_created)
            document_key = self.packing_document.pk

        if self.pk is None:
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
                StockChangeSet.construct(description="Stock supplication by {}".format(document_key), entries=entry, enum=enum["supplication"])
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
        return "Packing Document: {}, SupplierOrderLine: {}, ArticleType: {}, SupOrdCost: {}, InvoiceCost: {}, Invoice: {}".format(
            packing_doc, sol, self.article_type, cost, final_cost, invoice
        )


class DistributionStrategy:

    @staticmethod
    @transaction.atomic
    def distribute(user, supplier, distribution, document_identifier, invoice_identifier=False, indirect=False):
        """
        Distributes the actual packing document. A line_cost_after invoice should never be used if there is not direct invoice
        possible, indicated by the invoice_identifier. Distribution will refuse to execute in this case.
        :param user: The user that caused this distribution
        :param supplier: The supplier that ships the products
        :param distribution: List[PackingDocumentLine], with each PackingDocumentLine
        :param document_identifier: String, name of the packing document
        :param invoice_identifier: String, can be empty if there is no invoice
        :param indirect: Indirection flag. Function is only meant to be called indirectly. Change at your own peril.
        :return:
        """
        if not indirect:
            raise IndirectionError("Distribute must be called indirectly")
        assert user and isinstance(user, User)
        assert supplier and isinstance(supplier, Supplier)
        assert distribution and isinstance(distribution, list)
        assert document_identifier and isinstance(document_identifier, str)
        # Indicates that we are using an invoice in the process
        if invoice_identifier:
            assert isinstance(invoice_identifier, str)

        found_final_cost = False
        for pac_doc_line in distribution:
            assert pac_doc_line and isinstance(pac_doc_line, PackingDocumentLine)
            # Asserts correct article type and supplier consistency
            assert pac_doc_line.supplier_order_line
            assert pac_doc_line.article_type == pac_doc_line.supplier_order_line.article_type
            assert supplier == pac_doc_line.supplier_order_line.supplier_order.supplier
            # There cannot be a final cost without an invoice
            if not invoice_identifier:
                assert not hasattr(pac_doc_line, 'line_cost_after_invoice') or not pac_doc_line.line_cost_after_invoice
            if hasattr(pac_doc_line, 'line_cost_after_invoice') and pac_doc_line.line_cost_after_invoice is not None:
                found_final_cost = True

        if invoice_identifier:
            # Checks if there is an actual final_line_cost for a pac_doc_line to create an invoice for
            assert found_final_cost
            invoice = Invoice(supplier=supplier, supplier_identifier=invoice_identifier, user_modified=user)

        # Below here are the actual saves
        # First, saves of related documents
        packing_document = PackingDocument(supplier=supplier, supplier_identifier=document_identifier, user_modified=user)
        packing_document.save()
        if invoice_identifier:
            invoice.save()
        # Saves and final parameter settings of packing document lines
        for pac_doc_line in distribution:
            pac_doc_line.packing_document = packing_document
            if hasattr(pac_doc_line, 'line_cost_after_invoice') and pac_doc_line.line_cost_after_invoice:
                pac_doc_line.invoice = invoice
            pac_doc_line.user_modified = user
            pac_doc_line.save()

    @staticmethod
    def get_distribution(article_type_number_combos, supplier):
        """
        Creates a distribution
        :param article_type_number_combos: List[ArticleType, number, [Cost]]. A list containing articletypes, a multiplicity of thos
        article types, and a cost if the packing document line is connected to an invoice.
        :return:
        """
        raise UnimplementedError("Function does not exist at the super level. Call actual strategies")


class FirstSupplierOrderStrategy(DistributionStrategy):

    @staticmethod
    def get_distribution(article_type_number_combos, supplier):
        distribution = []
        # Viability assertions
        assert isinstance(supplier, Supplier)
        articletype_dict = defaultdict(lambda: 0)
        use_cost = False # Indicates that invoice, provided costs are used
        ARTICLE_TYPE_LOCATION=0
        NUMBER_LOCATION=1
        COST_LOCATION=2
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
            assert not articletype_dict[typ] > article_demand[typ]
        # Create the packing_document_lines
        for sol in relevant_supplier_orderline:
            if article_supply[sol.article_type] > 0:
                pac_doc_line = PackingDocumentLine(article_type=sol.article_type,
                                              line_cost=sol.line_cost
                                              ,supplier_order_line=sol)
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

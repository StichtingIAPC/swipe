from django.db import models, transaction
from crm.models import User
from stock.enumeration import enum
from supplier.models import Supplier, ArticleTypeSupplier
from logistics.models import SupplierOrderLine, SupplierOrderCombinationLine, InsufficientDemandError, IndirectionError
from money.models import CostField, Cost
from stock.models import StockChangeSet
from stock.stocklabel import OrderLabel
from article.models import ArticleType
from blame.models import ImmutableBlame, Blame
from collections import defaultdict


class PackingDocument(ImmutableBlame):

    timestamp = models.DateTimeField(auto_now=True)

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

    timestamp = models.DateTimeField(auto_now=True)


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
        Save function for a packing document line. WARNING: Does not modify the stock!
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
        return "Packing Document: {}, SupplierOrderLine: {}, ArticleType: {}, SupOrdCost: {}, InvoiceCost: {}, Invoice: {}".format(
            self.packing_document.pk, self.supplier_order_line.pk, self.article_type, cost, final_cost, invoice
        )


class DistributionStrategy:

    @staticmethod
    def distribute(user, supplier, distribution, document_identifier, invoice_identifier=False, indirect=False):
        """
        Distributes the actual packing document
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
        for pac_doc in distribution:
            assert pac_doc and isinstance(pac_doc, PackingDocumentLine)
            assert pac_doc.supplier_order_line

    @staticmethod
    def get_distribution():
        pass


class FirstSupplierOrderStrategy(DistributionStrategy):

    @staticmethod
    def get_distribution():
        pass

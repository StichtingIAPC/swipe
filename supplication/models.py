from django.db import models, transaction
from crm.models import User
from supplier.models import Supplier, ArticleTypeSupplier
from logistics.models import SupplierOrderLine
from money.models import CostField, Cost
from stock.models import StockChangeSet
from stock.stocklabel import OrderLabel
from article.models import ArticleType


class PackingDocument(models.Model):

    user = models.ForeignKey(User, on_delete=models.PROTECT)

    timestamp = models.DateTimeField(auto_now=True)

    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)

    supplier_identifier = models.CharField(max_length=30)

    @staticmethod
    @transaction.atomic
    def create_packing_document(user, supplier, packing_document_name, article_type_cost_combination, invoice_name=None):
        """
        Creates a packing document from the supplied information. This registers that the products have arrived at the store.
        It is linked to a single supplier, since that is the way you process packing documents.
        :param user:
        :param supplier:
        :param packing_document_name:
        :param article_type_cost_combination:
        :param invoice_name:
        :return:
        """


class Invoice(models.Model):

    supplier_identifier = models.CharField(max_length=30)

    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)

    user = models.ForeignKey(User, on_delete=models.PROTECT)

    timestamp = models.DateTimeField(auto_now=True)


class PackingDocumentLine(models.Model):
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
    def save(self):
        """
        Save function for a packing document line. WARNING: Does not modify the stock!
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
        # Mod supplierOrderLine
        self.supplier_order_line.mark_as_arrived(self.packing_document.user)
        if self.supplier_order_line.order_line is not None:
            # If there's a customer order, we also mark it as arrived
            self.supplier_order_line.order_line.arrive_at_store(self.packing_document.user)

        pk = self.packing_document.pk
        super(PackingDocumentLine, self).save()
        # Modify stock
        # TODO Remove the stock modification and move it to a function
        entry = [{
            'article': self.supplier_order_line.article_type,
            'book_value': self.line_cost,
            'count': 1,
            'is_in': True

        }]
        if hasattr(self.supplier_order_line, 'order_line') and self.supplier_order_line.order_line is not None:
            label = OrderLabel(self.supplier_order_line.order_line.order.pk)
            entry[0]['label'] = label
        StockChangeSet.construct(description="Stock supplication", entries=entry, enum=pk)

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


class DistributionStrategy():

    def distribute(self):
        pass

    def get_distribution(self):
        pass

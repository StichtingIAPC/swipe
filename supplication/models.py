from django.db import models, transaction
from crm.models import User
from supplier.models import Supplier
from logistics.models import SupplierOrderLine
from money.models import CostField, Cost


class PackingDocument(models.Model):

    user = models.ForeignKey(User)

    timestamp = models.DateTimeField(auto_now=True)

    supplier = models.ForeignKey(Supplier)


class PackingDocumentLine(models.Model):

    packing_document = models.ForeignKey(PackingDocument)

    supplier_order_line = models.ForeignKey(SupplierOrderLine)

    cost = CostField(null=True)

    @transaction.atomic
    def save(self):
        assert self.packing_document
        assert isinstance(self.packing_document, PackingDocument)
        assert self.supplier_order_line
        assert isinstance(self.supplier_order_line, SupplierOrderLine)
        if self.cost is not None:
            assert isinstance(self.cost, Cost)

        stock_cost = None
        # All assertions done, now we save everything
        if self.cost is not None:
            # Retrieve Cost from PackingDocumentLine
            pass
        else:
            # Retrieve Cost from SupplierOrderLine
            pass

        self.supplier_order_line.mark_as_arrived()


class DistributionStrategy():

    def distribute(self):
        pass

    def get_distribution(self):
        pass
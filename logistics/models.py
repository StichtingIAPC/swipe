from django.db import models, transaction
from supplier.models import Supplier, ArticleTypeSupplier
from order.models import OrderLine
from crm.models import User
from article.models import ArticleType, OrProductType


class SupplierOrder(models.Model):
    """
    Order we place at a supplier
    """
    supplier = models.ForeignKey(Supplier)

    copro = models.ForeignKey(User)


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
        assert self.supplier_article_type.supplier == self.supplier_order.supplier # Article can be ordered at supplier

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

    article_type = models.ForeignKey(ArticleType)

    number = models.IntegerField()

    stock_wish = models.ForeignKey()

    def save(self):
        assert self.number is not 0
        if self.pk is None:
            if self.number > 0:
                StockWishTable.add_products_to_table(self.article_type, self.number)
            else:
                StockWishTable.remove_products_from_table(self.article_type, -1 * self.number)
            super(StockWishLine, self).save()

        # Immutable after storage to prevent backlogging


class StockWish(models.Model):

    copro = models.ForeignKey(User)

    timestamp = models.DateTimeField(auto_now_add=True)


class StockWishTableLine(models.Model):

    article_type = models.ForeignKey(ArticleType, primary_key=True)

    number = models.IntegerField()


class StockWishTable:

    @staticmethod
    def add_products_to_table(article_type, number):
        article_type_status = StockWishTableLine.objects.get(article_type=article_type)
        if len(article_type_status) == 0:
            swtl = StockWishTableLine(article_type=article_type, number=number)
            swtl.save()
        else:
            article_type_status[0].number += number
            article_type_status[0].save()

    @staticmethod
    def remove_products_from_table(article_type, number):
        article_type_status = StockWishTableLine.objects.get(article_type=article_type)
        if len(article_type_status) == 0:
            raise CannotRemoveFromWishTableError("ArticleType is not included in table")
        else:
            if article_type_status[0].number < number:
                raise CannotRemoveFromWishTableError("Less ArticleTypes present than removal number")
            else:
                article_type_status[0].number -= number
                article_type_status[0].save()


class UnimplementedError(Exception):
    pass


class CannotRemoveFromWishTableError(Exception):
    pass

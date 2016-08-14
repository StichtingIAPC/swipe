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
        assert self.stock_wish is not None  # Pre-check, assumed from here on out
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

    copro = models.ForeignKey(User)

    timestamp = models.DateTimeField(auto_now_add=True)


class StockWishTableLine(models.Model):

    article_type = models.ForeignKey(ArticleType, primary_key=True)

    number = models.IntegerField()

    def save(self, indirect=False):
        if not indirect:
            raise IndirectionError("StockWishTableLine must be called indirectly from StockWishTable")
        else:
            super(StockWishTableLine, self).save()


class StockWishTable:

    @staticmethod
    def add_products_to_table(article_type, number, indirect=False,
                              stock_wish=None, supplier_order=None):
        if not indirect:
            raise IndirectionError("add_products_to_table must be called indirectly")
        article_type_status = StockWishTableLine.objects.get(article_type=article_type)
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

    number = models.IntegerField()

    article_type = models.ForeignKey(ArticleType)

    supplier_order = models.ForeignKey(SupplierOrder, null=True)

    stock_wish = models.ForeignKey(StockWish, null=True)

    def save(self, indirect=False):
        if not indirect:
            raise IndirectionError("Saving must be done indirectly")
        assert (self.supplier_order or self.stock_wish) and not(self.supplier_order and self.stock_wish)
        # ^ reason is either supplier order or stock wish modification
        super(StockWishTableLog, self).save()


class UnimplementedError(Exception):
    pass


class CannotRemoveFromWishTableError(Exception):
    pass


class IndirectionError(Exception):
    pass

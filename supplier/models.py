from django.db import models
from django.utils.translation import ugettext as _

from article.models import ArticleType
from money.models import CostField


class Supplier(models.Model):
    """
    Suppliers can provide the organisation with articles. This class stores the information related to the supplier
    """

    # Supplier name
    name = models.CharField(max_length=255, verbose_name=_("Supplier"))

    # URL for the search engine
    search_url = models.CharField(max_length=255, verbose_name=_("Search URL"), blank=True)

    # Notes about this supplier
    notes = models.TextField(verbose_name=_("Notes"), blank=True)

    # Is this supplier used
    is_used = models.BooleanField(default=True, verbose_name=_("This supplier is used"))

    # This supplier is a backup supplier
    is_backup = models.BooleanField(default=False, verbose_name=_("This supplier is a backup supplier"))

    # Last modified field
    last_modified = models.DateTimeField(auto_now=True, verbose_name=_("Last modified"))

    # This supplier is (soft)deleted
    is_deleted = models.BooleanField(default=False, verbose_name=_("This supplier is soft-deleted"))

    def __str__(self):
        return self.name


class ArticleTypeSupplier(models.Model):
    """
    Class for connecting the local ArticleType to its instance for the supplier. Provides info on cost and
    availability of products at the supplier
    """
    AVAILABILITY_OPTIONS = ('A', 'S', 'L', 'U', 'D')
    AVAILABILITY_OPTIONS_MEANINGS = {
        'A': 'Available at Supplier',
        'S': 'Soon available',
        'L': 'Later available',
        'U': 'Unknown availability',
        'D': 'Defunct product'
    }

    supplier = models.ForeignKey(Supplier)

    article_type = models.ForeignKey(ArticleType)

    cost = CostField()  # Describes the cost of

    minimum_number_to_order = models.IntegerField()

    supplier_string = models.CharField(primary_key=True, max_length=255)

    availability = models.CharField(max_length=255, choices=sorted(AVAILABILITY_OPTIONS_MEANINGS.items()))

    class Meta:
        unique_together = ['supplier', 'article_type']

    def has_graduated_pricing(self):
        gps = VolumeDiscountPricing.objects.filter(article_type_supplier=self)
        return len(gps) > 0


class VolumeDiscountPricing(models.Model):
    """
    Sometimes products become cheaper if ordered in larger quantities. This can be stored in graduated pricing
    schemes, such as this one.
    """

    article_type_supplier = models.ForeignKey(ArticleTypeSupplier)

    number = models.IntegerField()

    cost_per_item = CostField()

    class Meta:
        unique_together = ['article_type_supplier', 'number']


class SupplierTypeArticle(models.Model):
    """
    Information a supplier gives about its own products. Can be updated with price lists or manually.
    """

    article_type_supplier = models.ForeignKey(ArticleTypeSupplier, null=True)

    number = models.CharField(max_length=100)

    name = models.CharField(max_length=255)

    ean = models.IntegerField(null=True)

    cost = CostField(null=True)  # Describes the cost of

    minimum_number_to_order = models.IntegerField(null=True)

    supply = models.IntegerField(null=True)

    packing_amount = models.IntegerField(null=True)

    def __str__(self):
        return "ArtTypSupId: {}, sup_number: {}, name: {}, ean: {}, cost: {}, minimum_order: {}, " \
               "supply: {}, packing_amount: {}".format(self.article_type_supplier_id, self.number,
                                                       self.name, self.ean, self.cost, self.minimum_number_to_order,
                                                       self.supply, self.packing_amount)

from django.db import models
from django.utils.translation import ugettext as _
from django.utils import timezone

from article.models import ArticleType
from money.models import CostField

from tools.util import raiseifnot

import datetime


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
    # The supplier of this information
    supplier = models.ForeignKey(Supplier)
    # The article type linked
    article_type = models.ForeignKey(ArticleType)

    cost = CostField()  # Describes the cost of

    minimum_number_to_order = models.IntegerField()

    supplier_string = models.CharField(max_length=255)

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

    # A connection to a product in our own assortment via ArticleTypeSupplier
    article_type_supplier = models.OneToOneField(ArticleTypeSupplier, null=True)
    # The supplier of an article
    supplier = models.ForeignKey(Supplier)
    # The unique identifier of the supplier for this product
    number = models.CharField(max_length=100)
    # The textual representation("name") of the article
    name = models.CharField(max_length=255)
    # Unique numerical identifier, is a 14 digit long number
    ean = models.IntegerField(null=True)
    # The price for which we can buy the product
    cost = CostField(null=True)
    # The minimum number of articles you can order of this product
    minimum_number_to_order = models.IntegerField(null=True)
    # How much articles are in stock
    supply = models.IntegerField(null=True)
    # Articles are sold in multiples of the packing amount
    packing_amount = models.IntegerField(null=True)
    # Date this article was updated
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return "SupplierId: {}, ArtTypSupId: {}, sup_number: {}, name: {}, ean: {}, cost: {}, minimum_order: {}, " \
               "supply: {}, packing_amount: {}".format(self.supplier_id, self.article_type_supplier_id, self.number,
                                                       self.name, self.ean, self.cost, self.minimum_number_to_order,
                                                       self.supply, self.packing_amount)

    @staticmethod
    def process_supplier_type_articles(supplier_type_articles):
        """
        Processes SupplierTypeArticles and updates the list of products for one supplier. In the ideal case, old data would be
        overwritten by new data. Experience does tell that this does not work. Therefore, some basic checks need to be done
        :param supplier_type_articles:
        :type supplier_type_articles: list[SupplierTypeArticle]
        :return: A list of supplierTypeArticles that can be written back to the database
        """
        if len(supplier_type_articles) > 0:
            supplier = supplier_type_articles[0].supplier
        else:
            return

        # Basic sanity checks, fail quickly if an error occurs
        for sta in supplier_type_articles:
            raiseifnot(isinstance(sta, SupplierTypeArticle), TypeError, "sta should be a SupplierTypeArticle")
            raiseifnot(sta.supplier == supplier, SupplierTypeArticleProcessingError, "Supplier is not uniform")

        CLEAN_UP_LIMIT = 31

        cutoff_date = datetime.date.today() - datetime.timedelta(days=CLEAN_UP_LIMIT)

        # Removes all SupplierTypeArticles that are out of date. After {x} days, we can safely assume
        # that the data holds no significance to the assortment.
        SupplierTypeArticle.objects.filter(date_updated__lt=cutoff_date, supplier=supplier).delete()

        old_supplier_articles = SupplierTypeArticle.objects.filter(supplier=supplier)
        old_art_dict = {}

        for oldy in old_supplier_articles:
            old_art_dict[oldy.number] = oldy

        # Two lists: First is the list of old articles that can deleted because the new article has superseded
        # the old one or the old is not found in the list any more. The new arts are the articles that renew an
        # old line or are new in the price list
        old_arts_to_be_deleted = []  # type: list[SupplierTypeArticle]
        new_arts_to_be_added = []  # type: list[SupplierTypeArticle]

        for sta in supplier_type_articles:
            old_ver = old_art_dict.get(sta.number)
            if not old_ver:
                sta.date_updated = timezone.now()
                new_arts_to_be_added.append(sta)
            else:
                # We have a match for an old article and a new article
                # We must check if the details are similar enough to detect a match
                # If the details match is dubious, the new data must be rejected
                pass

        # IDs of STAs to be deleted
        delete_ids = []  # type: list[int]
        for art in old_arts_to_be_deleted:
            delete_ids.append(art.id)

        # Delete old articles in one go
        SupplierTypeArticle.objects.filter(id__in=delete_ids).delete()
        # Create new articles in one go
        SupplierTypeArticle.objects.bulk_create(new_arts_to_be_added)


class SupplierTypeArticleProcessingError(Exception):
    pass

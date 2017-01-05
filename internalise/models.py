from django.db import models
from blame.models import ImmutableBlame, Blame
from article.models import ArticleType
from money.models import CostField
from crm.models import User
from tools.util import raiseif
from collections import defaultdict
from stock.models import Stock, StockChangeSet
from stock.enumeration import enum


class InternaliseDocument(Blame):
    """
    A way to use products for internal usage. Can be taken from any present article in the stockTable, including
    reserved places with a label like an order. The should be used for assigning products for internal usage and
    not as a magical way of reducing the stock.
    """
    # A memo which can contain the explanation for the usage of the products.
    memo = models.TextField()

    @staticmethod
    def create_internal_products_document(user: User, articles_with_information: list, memo: str):
        """

        :param user: The user who commanded the change.
        :param articles_with_information: The information needed to effectuate the internalisation.
                                           Count should be strictly positive. Labels should null for stock.
        :type articles_with_information: list(tuple(articleType, count, label_type StockLabel, label_key integer))
        :param memo: The memo which is used as the description
        """
        raiseif(not isinstance(user, User), DataTypeError, "user is not a User")
        raiseif(not isinstance(memo, str), DataTypeError, "memo is not a str")

        article_demand = defaultdict(lambda: 0)
        for article, count, label_type, label_key in articles_with_information:
            raiseif(not isinstance(article, ArticleType), DataTypeError, "article should be an ArticleType")
            raiseif(not isinstance(count, int), DataTypeError, "count should be an int")
            raiseif(count <= 0, DataValidityError, "count should be greater than 0")
            if (label_type and (not label_key or label_key <= 0)) or (not label_type and label_key):
                raise DataValidityError("Cannot gage if label is used or not")
            article_demand[(article, label_type, label_key)] += count

        internal_lines = []
        stock_mod_entries = []

        for article, label_type, label_key in article_demand.keys():
            if label_type:
                # noinspection PyProtectedMember
                st = Stock.objects.get(article=article, labeltype=label_type.labeltype, labelkey=label_key)
                if st.count < article_demand[(article, label_type, label_key)]:
                    raise DataValidityError("Tried to internalise {} for article {} with keytype {} and value {}"
                                            "but only {} is present".format(article_demand[(article, label_type,
                                                                                            label_key)], article,
                                                                            label_type, label_key, st.count))
                else:
                    # noinspection PyProtectedMember
                    internal_lines.append(InternaliseLine(article_type=article,
                                                          label_type=label_type.labeltype,
                                                          identifier=label_key,
                                                          cost=st.book_value,
                                                          count=article_demand[(article, label_type, label_key)],
                                                          user_modified=user))
                    stock_mod_entries.append({
                        'article': article,
                        'book_value': st.book_value,
                        'count': article_demand[(article, label_type, label_key)],
                        'label': label_type(label_key),
                        'is_in': False
                    })

            else:
                st = Stock.objects.get(article=article, labelkey__isnull=True)
                if st.count < article_demand[(article, label_type, label_key)]:
                    raise DataValidityError("Tried to internalise {} for articleType {} from stock while stock only"
                                            "contains {} products".format(article_demand[(article, label_type,
                                                                                          label_key)],
                                                                          article, st.count))
                else:
                    internal_lines.append(InternaliseLine(article_type=article, label_type=None, identifier=None,
                                                          count=article_demand[(article, label_type, label_key)],
                                                          cost=st.book_value, user_modified=user))
                    stock_mod_entries.append({
                        'article': article,
                        'book_value': st.book_value,
                        'count': article_demand[(article, label_type, label_key)],
                        'is_in': False
                    })

        # We now have everything we need. Let's save
        doc = InternaliseDocument(memo=memo, user_modified=user)
        doc.save()
        for line in internal_lines:
            line.internalise_document = doc
            line.save()

        StockChangeSet.construct(description="Internalisation with document {}".format(doc.pk),
                                 entries=stock_mod_entries,
                                 enum=enum['internalise'])


class InternaliseLine(ImmutableBlame):
    """
    A line which contains the neccesary information about the products taken from stock. This is to be used as a way of
    logging products that are used for internal consumption.
    """
    # The document to bind the lines together
    internalise_document = models.ForeignKey(InternaliseDocument)
    # The articleType to be used
    article_type = models.ForeignKey(ArticleType)
    # The amount
    count = models.IntegerField()
    # The cost(excluding VAT) for using a single product. Will be retrieved from stock for storage in creation function.
    cost = CostField()
    # The labelType unique identifier to retrieve the product. Null for stock
    label_type = models.CharField(max_length=255, null=True)
    # If a labelType is used, this should be used(not Null, >0) to identify the StockLine. Null for stock.
    identifier = models.IntegerField(null=True)


class DataTypeError(Exception):
    pass


class DataValidityError(Exception):
    pass


class IndirectionError(Exception):
    pass

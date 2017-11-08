# Create your views here.
import json

from decimal import Decimal
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import generics
from rest_framework import mixins

from article.models import ArticleType
from logistics.models import SupplierOrder, SupplierOrderLine, SupplierOrderState, StockWishTableLog, StockWish
from logistics.serializers import SupplierOrderSerializer, SupplierOrderLineSerializer, SupplierOrderStateSerializer, StockWishTableLogSerializer, \
    StockWishSerializer
from money.models import Cost
from supplier.models import Supplier
from tools.util import raiseif


class SupplierOrderListView(mixins.ListModelMixin,
                      generics.GenericAPIView):
    serializer_class = SupplierOrderSerializer

    def get_queryset(self):
        return SupplierOrder.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        supplierorder_request = SupplierOrderRequest(user_modified=request.data.get("user_modified"),
                                                     articles_ordered_list=request.data.get("articles_ordered"),
                                                     allow_different_system_currency=request.data.get("allow_different_currency"),
                                                     supplier=request.data.get("supplier"))
        supplierorder_representation = SupplierOrderSerializer(instance=supplierorder_request.create_supplierorder_request()).data
        return HttpResponse(content=json.dumps(supplierorder_representation), content_type="application/json")

class SupplierOrderRequest:

    def __init__(self, user_modified: int, articles_ordered_list: list, supplier: int, allow_different_system_currency: bool):
        self.user_modified = user_modified
        raiseif(not isinstance(user_modified, int), "User is not of type int")
        self.supplier = supplier
        raiseif(not isinstance(supplier, int), "Supplier is not of type int")
        self.allow_different_system_currency = allow_different_system_currency
        raiseif(not isinstance(allow_different_system_currency, bool), "allow_different_system_currency is not of type bool")
        self.articles_ordered = []
        for article_id, amount, cost in articles_ordered_list:
            self.articles_ordered.append(SupplierOrderRequest.OrderedArticle(article_id=article_id,
                                                                             amount=amount,
                                                                             cost=cost))

    def create_supplierorder_request(self):
        user = User.objects.get(id=self.user_modified)
        supplier = Supplier.objects.get(id=self.supplier)
        arts_ordered = []
        for article_ordered in self.articles_ordered:
            arts_ordered.append(article_ordered.to_model_data())
        return SupplierOrder.create_supplier_order(user_modified=user, supplier=supplier, articles_ordered=arts_ordered,
                                                   allow_different_currency=self.allow_different_system_currency)


    class OrderedArticle:

        def __init__(self, article_id: int, amount: int, cost):
            self.article_id = article_id
            raiseif(not isinstance(article_id, int), "article_id is not of type int")
            self.amount = amount
            raiseif(not isinstance(amount, int), "amount is not of type int")
            self.cost = cost

        def to_model_data(self):
            article = ArticleType.objects.get(pk=self.article_id)
            cost = Cost(amount=Decimal(self.cost.get("amount")), currency=self.cost.get("currency"),
                        use_system_currency=self.cost.get("use_system_currency"))
            return [article, self.amount, cost]


class SupplierOrderView(mixins.RetrieveModelMixin,
                        generics.GenericAPIView):
    serializer_class = SupplierOrderSerializer

    def get_queryset(self):
        return SupplierOrder.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class SupplierOrderLineListView(mixins.ListModelMixin,
                                generics.GenericAPIView):
    serializer_class = SupplierOrderLineSerializer

    def get_queryset(self):
        return SupplierOrderLine.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SupplierOrderLineView(mixins.RetrieveModelMixin,
                                generics.GenericAPIView):
    serializer_class = SupplierOrderLineSerializer

    def get_queryset(self):
        return SupplierOrderLine.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class SupplierOrderStateListView(mixins.ListModelMixin,
                                generics.GenericAPIView):
    serializer_class = SupplierOrderStateSerializer

    def get_queryset(self):
        return SupplierOrderState.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SupplierOrderStateByStateView(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               generics.GenericAPIView):
        serializer_class = SupplierOrderStateSerializer

        def get_queryset(self):
            return SupplierOrderState.objects.filter(state=self.kwargs['state'])

        def get(self, request, *args, **kwargs):
            return self.list(request, *args, **kwargs)


class SupplierOrderStateBySupplierOrderLineView(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               generics.GenericAPIView):
        serializer_class = SupplierOrderStateSerializer

        def get_queryset(self):
            return SupplierOrderState.objects.filter(supplier_order_line_id=self.kwargs['supplier_order_line_pk'])

        def get(self, request, *args, **kwargs):
            return self.list(request, *args, **kwargs)


class SupplierOrderStateView(mixins.RetrieveModelMixin,
                            generics.GenericAPIView):
    serializer_class = SupplierOrderStateSerializer

    def get_queryset(self):
        return SupplierOrderState.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class StockWishView(mixins.CreateModelMixin,
                    generics.GenericAPIView):
    serializer_class = StockWishSerializer

    def post(self, request, *args, **kwargs):
        stockwish_request = StockWishRequest(user=request.data.get("user_modified"),
                                             articles_ordered_list=request.data.get("articles_ordered"))
        stockwish_representation = StockWishSerializer(instance=stockwish_request.create_stockwish_request()).data
        return HttpResponse(content=json.dumps(stockwish_representation), content_type="application/json")


class StockWishRequest:

    def __init__(self, user: int, articles_ordered_list: list,):
        raiseif(not isinstance(user, int), "User is not of type int")
        self.user = user
        self.articles_ordered = []
        for article_id, amount_ordered in articles_ordered_list:
            self.articles_ordered.append(StockWishRequest.ArticlesOrderedInformation(
                article_id=article_id, amount_ordered=amount_ordered
            ))

    def create_stockwish_request(self):
        user = User.objects.get(id=self.user)
        arts_ordered = []
        for article_ordered in self.articles_ordered:
            arts_ordered.append(article_ordered.to_model_data())
        return StockWish.create_stock_wish(user_modified=user, articles_ordered=arts_ordered)

    class ArticlesOrderedInformation:

        def __init__(self, article_id: int, amount_ordered: int):
            self.article_id = article_id
            raiseif(not isinstance(article_id, int), "article_id is not of type int")
            self.amount_ordered = amount_ordered
            raiseif(not isinstance(amount_ordered, int), "amount_ordered is not of type int")

        def to_model_data(self):
            article = ArticleType.objects.get(pk=self.article_id)
            return (article, self.amount_ordered)


class StockWishTableLogListView(mixins.ListModelMixin,
                                generics.GenericAPIView):
    serializer_class = StockWishTableLogSerializer

    def get_queryset(self):
        return StockWishTableLog.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class StockWishTableLogView(mixins.RetrieveModelMixin,
                                generics.GenericAPIView):
    serializer_class = StockWishTableLogSerializer

    def get_queryset(self):
        return StockWishTableLog.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class StockWishTableLogViewByStockWish(mixins.ListModelMixin,
                                generics.GenericAPIView):
    serializer_class = StockWishTableLogSerializer

    def get_queryset(self):
        return StockWishTableLog.objects.filter(stock_wish_id=self.kwargs.get("stock_wish_id"))

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)



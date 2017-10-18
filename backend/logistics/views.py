# Create your views here.
import json

from decimal import Decimal
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse
from rest_framework import generics
from rest_framework import mixins

from article.models import ArticleType
from logistics.models import SupplierOrder, SupplierOrderLine, SupplierOrderState, StockWishTableLog, StockWish
from logistics.serializers import SupplierOrderSerializer, SupplierOrderLineSerializer, SupplierOrderStateSerializer, StockWishTableLogSerializer, \
    StockWishSerializer
from money.models import Cost
from supplier.models import Supplier


class SupplierOrderListView(mixins.ListModelMixin,
                      generics.GenericAPIView):
    queryset = SupplierOrder.objects.all()
    serializer_class = SupplierOrderSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # move this post method to SupplierOrderView?
    def post(self, request, *args, **kwargs):
        self.user = User.objects.get(id=request.data.get("user_modified"))
        self.articles_ordered = request.data.get("articles_ordered")
        resultset = []
        for article_id, number, cost in self.articles_ordered:
            entry = []
            article = ArticleType.objects.get(id=article_id)
            cost = Cost(amount=Decimal(cost.get("amount")), currency=cost.get("currency"), use_system_currency=cost.get("use_system_currency"))
            entry.append(article)
            entry.append(number)
            entry.append(cost)
            resultset.append(entry)
        self.allow_different_currency = request.data.get("allow_different_currency")
        self.supplier = Supplier.objects.get(id=request.data.get("supplier"))
        supplierorder = SupplierOrder.create_supplier_order(user_modified=self.user,
                                                            supplier=self.supplier,
                                                            articles_ordered=resultset,
                                                            allow_different_currency=self.allow_different_currency)
        # was not able to directly serialize... maybe try to find a better way to do this?
        supplierorder_json = json.dumps({"user_created": supplierorder.user_created.id,
                                        "supplier": supplierorder.supplier.id})
        return HttpResponse(content=supplierorder_json, content_type="application/json")


class SupplierOrderView(mixins.RetrieveModelMixin,
                        generics.GenericAPIView):
    queryset = SupplierOrder.objects.all()
    serializer_class = SupplierOrderSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class SupplierOrderLineListView(mixins.ListModelMixin,
                                generics.GenericAPIView):
    queryset = SupplierOrderLine.objects.all()
    serializer_class = SupplierOrderLineSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SupplierOrderLineView(mixins.RetrieveModelMixin,
                                generics.GenericAPIView):
    queryset = SupplierOrderLine.objects.all()
    serializer_class = SupplierOrderLineSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class SupplierOrderStateListView(mixins.ListModelMixin,
                                generics.GenericAPIView):
    queryset = SupplierOrderState.objects.all()
    serializer_class = SupplierOrderStateSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SupplierOrderStateByStateView(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               generics.GenericAPIView):
        serializer_class = SupplierOrderStateSerializer

        def get(self, request, *args, **kwargs):
            self.queryset = SupplierOrderState.objects.filter(state=kwargs['state'])
            resultset = []
            for element in self.queryset:
                resultset.append(element)
            return HttpResponse(content=serializers.serialize('json', resultset, indent=4),
                                content_type="application/json")


class SupplierOrderStateBySupplierOrderLineView(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               generics.GenericAPIView):
        serializer_class = SupplierOrderStateSerializer

        def get(self, request, *args, **kwargs):
            self.queryset = SupplierOrderState.objects.filter(supplier_order_line_id=kwargs['supplier_order_line_pk'])
            resultset = []
            for element in self.queryset:
                resultset.append(element)
            return HttpResponse(content=serializers.serialize('json', resultset, indent=4),
                                content_type="application/json")


class SupplierOrderStateView(mixins.RetrieveModelMixin,
                            generics.GenericAPIView):
    queryset = SupplierOrderState.objects.all()
    serializer_class = SupplierOrderStateSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class StockWishView(mixins.CreateModelMixin,
                    generics.GenericAPIView):
    serializer_class = StockWish

    def post(self, request, *args, **kwargs):
        self.user = User.objects.get(id=request.data.get("user_modified"))
        self.articles_ordered = request.data.get("articles_ordered")
        resultset = []
        for article_id, number in self.articles_ordered:
            entry = []
            article = ArticleType.objects.get(id=article_id)
            entry.append(article)
            entry.append(number)
            resultset.append(entry)
        stockwish = StockWishSerializer(StockWish.create_stock_wish(user_modified=self.user, articles_ordered=resultset)).data
        return HttpResponse(content=json.dumps(stockwish), content_type="application/json")



class StockWishTableLogListView(mixins.ListModelMixin,
                                generics.GenericAPIView):
    queryset = StockWishTableLog.objects.all()
    serializer_class = StockWishTableLogSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class StockWishTableLogView(mixins.RetrieveModelMixin,
                                generics.GenericAPIView):
    queryset = StockWishTableLog.objects.all()
    serializer_class = StockWishTableLogSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class StockWishTableLogViewByStockWish(mixins.ListModelMixin,
                                generics.GenericAPIView):
    serializer_class = StockWishTableLogSerializer

    def get(self, request, *args, **kwargs):
        print(kwargs)
        self.queryset = StockWishTableLog.objects.filter(stock_wish_id=kwargs.get("stock_wish_id"))
        resultset = []
        for element in self.queryset:
            resultset.append(element)
        return HttpResponse(content=serializers.serialize('json', resultset, indent=4),
                            content_type="application/json")



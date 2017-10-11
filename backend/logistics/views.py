# Create your views here.
from django.core import serializers
from django.http import HttpResponse
from rest_framework import generics
from rest_framework import mixins

from logistics.models import SupplierOrder, SupplierOrderLine, SupplierOrderState, StockWishTableLog
from logistics.serializers import SupplierOrderSerializer, SupplierOrderLineSerializer, SupplierOrderStateSerializer, StockWishTableLogSerializer


class SupplierOrderListView(mixins.ListModelMixin,
                      generics.GenericAPIView):
    queryset = SupplierOrder.objects.all()
    serializer_class = SupplierOrderSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

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



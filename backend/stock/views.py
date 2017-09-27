from django.shortcuts import render
from rest_framework import mixins, generics

from crm.models import Customer
from stock.models import Stock
from stock.serializers import StockSerializer


class StockView(mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin,
                generics.GenericAPIView):
    queryset = Stock.objects.all().select_related('article')
    serializer_class = StockSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class StockListView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):
    queryset = Stock.objects.all().select_related('article')
    serializer_class = StockSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

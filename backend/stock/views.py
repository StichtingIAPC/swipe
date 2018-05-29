from django.shortcuts import render
from rest_framework import mixins, generics

from crm.models import Customer
from stock.models import Stock
from stock.serializers import StockSerializer
from www.models import SwipeLoginRequired


class StockView(SwipeLoginRequired, mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin,
                generics.GenericAPIView):
    queryset = Stock.objects.all().select_related('article')
    serializer_class = StockSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class StockListView(SwipeLoginRequired, mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):
    queryset = Stock.objects.all().select_related('article')
    serializer_class = StockSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

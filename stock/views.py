from django.shortcuts import render
from rest_framework import mixins, generics

from stock.models import Stock
from stock.serializers import StockSerializer

class StockView(mixins.UpdateModelMixin,
                          mixins.RetrieveModelMixin,
                          generics.GenericAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

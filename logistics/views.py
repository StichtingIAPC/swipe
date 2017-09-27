from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework import mixins

from logistics.models import SupplierOrder
from logistics.serializers import SupplierOrderSerializer


class SupplierOrderListView(mixins.ListModelMixin,
                      generics.GenericAPIView):
    queryset = SupplierOrder.objects.all()
    serializer_class = SupplierOrderSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
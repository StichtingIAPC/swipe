# Create your views here.
from rest_framework import generics
from rest_framework import mixins

from logistics.models import SupplierOrder, SupplierOrderLine
from logistics.serializers import SupplierOrderSerializer, SupplierOrderLineSerializer


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


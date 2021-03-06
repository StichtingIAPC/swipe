from rest_framework import mixins, generics

from supplier.models import Supplier
from supplier.serializers import SupplierSerializer
from www.models import SwipeLoginRequired


class SupplierListView(SwipeLoginRequired, mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SupplierView(SwipeLoginRequired, mixins.UpdateModelMixin,
                   mixins.RetrieveModelMixin,
                   generics.GenericAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

# Write your views here
from rest_framework import generics
from rest_framework import mixins

from order.models import *
from order.serializers import OrderSerializer, OrderLineSerializer


class OrderListView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OrderView(mixins.RetrieveModelMixin,
                generics.GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CustomerOrderView(mixins.RetrieveModelMixin,
                    generics.GenericAPIView):
    queryset = Order.objects.all().prefetch_related('customer')
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class OrderLineListView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):
    queryset = OrderLine.objects.all()
    serializer_class = OrderLineSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OrderLineView(mixins.RetrieveModelMixin,
                    generics.GenericAPIView):
    queryset = OrderLine.objects.all()
    serializer_class = OrderLineSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class OrderLineByStateView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):
    queryset = OrderLine.objects.all().prefetch_related('state')
    serializer_class = OrderLineSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
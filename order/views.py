# Write your views here
from django.core import serializers
from django.http import HttpResponse
from rest_framework import generics
from rest_framework import mixins
import json

from order.models import *
from order.serializers import OrderSerializer, OrderLineSerializer, OrderLineStateSerializer


class OrderListView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # customer, user, wishable
        pass

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
    serializer_class = OrderLineSerializer


    def get(self, request, *args, **kwargs):
        self.queryset = OrderLine.objects.filter(state=kwargs['state'])
        # moet nog ff naar gekeken worden
        resultset = []
        for element in self.queryset:
            resultset.append(element)
        return HttpResponse(content=serializers.serialize('json', resultset, indent=4), content_type="application/json")


class OrderLineStateListView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):
    queryset = OrderLineState.objects.all()
    serializer_class = OrderLineStateSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OrderLineStateView(mixins.RetrieveModelMixin,
                generics.GenericAPIView):
    queryset = OrderLineState.objects.all()
    serializer_class = OrderLineStateSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class OrderLineStateByStateView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):
    serializer_class = OrderLineStateSerializer


    def get(self, request, *args, **kwargs):
        self.queryset = OrderLineState.objects.filter(state=kwargs['state'])
        # moet nog ff naar gekeken worden
        resultset = []
        for element in self.queryset:
            resultset.append(element)
        return HttpResponse(content=serializers.serialize('json', resultset, indent=4), content_type="application/json")


class OrderLineStateByOrderLineView(mixins.ListModelMixin,
                generics.GenericAPIView):
    serializer_class = OrderLineStateSerializer

    def get(self, request, *args, **kwargs):
        self.queryset = OrderLineState.objects.filter(orderline=kwargs['orderline'])
        return self.list(request, *args, **kwargs)
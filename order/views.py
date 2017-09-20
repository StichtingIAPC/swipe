# Write your views here
from django.core import serializers
from django.http import HttpResponse
from rest_framework import generics
from rest_framework import mixins
import json

from money.serializers import PriceSerializer
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
        # customer, user, wishable_type_number_price_combinations(List[List[WishableType, number, Price]])
        order_request = OrderRequest(request.data.get('customer'), request.data.get('user'), request.data.get('wishable_type_number_price_combinations'))
        order_result = order_request.create_order()
        return HttpResponse(content=order_result, content_type="application/json")


class OrderRequest():

    def __init__(self, customer: int, user: int, wishable_type_number_price_combinations):
        self.customer = customer
        self.user = user
        self.wishable_type_number_price_combinations = wishable_type_number_price_combinations

    def create_order(self):
        customer = Customer.objects.get(id=self.customer)
        user = User.objects.get(id=self.user)
        wishable_type_number_price_combination_result_set = []
        for tuple in self.wishable_type_number_price_combinations:
            list_contents = []
            # append the WishableType
            list_contents.append(WishableType.objects.get(id=tuple[0]))
            # append the number
            list_contents.append(tuple[1])
            # append the price
            list_contents.append(PriceSerializer().to_internal_value(tuple[2]))
            wishable_type_number_price_combination_result_set.append(list_contents)
        created_order = Order.create_order_from_wishables_combinations(user=user, customer=customer, wishable_type_number_price_combinations=wishable_type_number_price_combination_result_set)
        return OrderSerializer().to_representation(created_order)

    def __str__(self):
        return "customer: {}, user: {} , wishable_type_number_price_combinations: {}".format(self.customer, self.user, self.wishable_type_number_price_combinations)


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
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
        order_request = OrderRequest(request.data.get('customer'), request.data.get('user'), request.data.get('wishable_type_number_price_combinations'))
        order_result = order_request.create_order()
        return HttpResponse(content=json.dumps(order_result), content_type="application/json")


class OrderRequest:

    class ArticleInformation:

        def __init__(self, wishable_type: int, amount: int, price):
            self.wishable_type = wishable_type
            self.amount = amount
            self.price = Price(amount=Decimal(price.get("amount")), vat=Decimal(price.get("vat")),
                               use_system_currency=True)

        def to_model_format(self):
            return (SellableType.objects.get(id=self.wishable_type), self.amount, self.price)

    def __init__(self, customer: int, user: int, wishable_type_number_price_combinations):
        raiseif(not isinstance(customer, int), InvalidDataError,
                "customer must be of type int, but it wasn't")
        raiseif(not isinstance(user, int), InvalidDataError,
                "user must be of type int, but it wasn't")
        raiseif(not isinstance(wishable_type_number_price_combinations, list), InvalidDataError,
                "wishable_type_number_price_combinations must be of type list, but it wasn't")
        self.customer = customer
        self.user = user
        self.wishable_type_number_price_combinations = wishable_type_number_price_combinations

    def create_order(self):
        customer = Customer.objects.get(id=self.customer)
        raiseif(customer is None, InvalidDataError,
                "the customer related to this order does not exist")
        user = User.objects.get(id=self.user)
        raiseif(customer is None, InvalidDataError,
                "the user to this order does not exist")
        wishable_type_number_price_combination_result_set = []
        for article_information_data in self.wishable_type_number_price_combinations:
            wishable_type = article_information_data.get("wishable_type")
            amount = article_information_data.get("amount")
            price = article_information_data.get("price")
            raiseif(wishable_type is None, InvalidDataError,
                    "wishable_type in wishable_type_number_price_combinations is None, but it should exist")
            raiseif(not isinstance(wishable_type, int), InvalidDataError,
                    "wishable_type in wishable_type_number_price_combinations should be of type int, but wishable_type was not int")
            raiseif(amount is None, InvalidDataError,
                    "amount in wishable_type_number_price_combinations is None, but it should exist")
            raiseif(not isinstance(amount, int), InvalidDataError,
                    "amount in wishable_type_number_price_combinations should be of type int, but amount was not int")
            raiseif(not amount > 0, InvalidDataError,
                    "amount in wishable_type_number_price_combinations should be larger than 0, but it isn't")
            raiseif(price is None, InvalidDataError,
                    "price in wishable_type_number_price_combinations is None, but it should exist")
            article_information = OrderRequest.ArticleInformation(wishable_type=wishable_type,
                                                                  amount=amount,
                                                                  price=price)
            wishable_type_number_price_combination_result_set.append(article_information.to_model_format())
        created_order = Order.create_order_from_wishables_combinations(user=user, customer=customer, wishable_type_number_price_combinations=wishable_type_number_price_combination_result_set)
        return OrderSerializer(created_order).data

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
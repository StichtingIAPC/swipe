from collections import OrderedDict

from rest_framework import mixins, generics

from money.models import CurrencyData, Denomination, VAT, AccountingGroup, Currency, Money, Price, Cost
from money.serializers import CurrencySerializer, DenominationSerializer, VATSerializer, AccountingGroupSerializer
from tools.json_parsers import ParseError, DictParsers


class MoneyDictParsers:

    @staticmethod
    def money_parser(obj: dict):
        if obj is None:
            raise ParseError("Money does not exist")
        if not isinstance(obj, dict):
            raise ParseError("Object cannot be a Money as it is not a dict")
        amount = DictParsers.decimal_parser(obj.get("amount"))
        currency = Currency(iso=DictParsers.string_parser(obj.get("currency")))
        return Money(amount=amount, currency=currency)

    @staticmethod
    def cost_parser(obj: dict):
        if obj is None:
            raise ParseError("Cost does not exist")
        if not isinstance(obj, dict):
            raise ParseError("Object cannot be a Cost as it is not a dict")
        amount = DictParsers.decimal_parser(obj.get("amount"))
        currency = Currency(iso=DictParsers.string_parser(obj.get("currency")))
        return Cost(amount=amount, currency=currency)

    @staticmethod
    def price_parser(obj:dict):
        if obj is None:
            raise ParseError("Price does not exist")
        if not isinstance(obj, dict):
            raise ParseError("Object cannot be a Price as it is not a dict")
        amount = DictParsers.decimal_parser(obj.get("amount"))
        currency = Currency(iso=DictParsers.string_parser(obj.get("currency")))
        vat = DictParsers.decimal_parser(obj.get("vat"))
        return Price(amount=amount, currency=currency, vat=vat)

class CurrencyListView(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):
    queryset = CurrencyData.objects.all() \
        .prefetch_related('denomination_set')
    serializer_class = CurrencySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CurrencyView(mixins.UpdateModelMixin,
                   mixins.RetrieveModelMixin,
                   generics.GenericAPIView):
    queryset = CurrencyData.objects.all() \
        .prefetch_related('denomination_set')
    serializer_class = CurrencySerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class DenominationDelete(mixins.DestroyModelMixin,
                         generics.GenericAPIView):
    queryset = Denomination.objects.all()
    serializer_class = DenominationSerializer


class VATListView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = VAT.objects.all() \
        .prefetch_related('vatperiod_set')
    serializer_class = VATSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class VATView(mixins.UpdateModelMixin,
              mixins.RetrieveModelMixin,
              generics.GenericAPIView):
    queryset = VAT.objects.all() \
        .prefetch_related('vatperiod_set')
    serializer_class = VATSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class AccountingGroupListView(mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              generics.GenericAPIView):
    queryset = AccountingGroup.objects.all()
    serializer_class = AccountingGroupSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AccountingGroupView(mixins.UpdateModelMixin,
                          mixins.RetrieveModelMixin,
                          generics.GenericAPIView):
    queryset = AccountingGroup.objects.all()
    serializer_class = AccountingGroupSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

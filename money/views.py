from rest_framework import mixins, generics

from money.models import CurrencyData, Denomination, VAT, VATPeriod
from money.serializers import CurrencySerializer, DenominationSerializer, VATSerializer, VATPeriodSerializer


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


class VATPeriodListView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        generics.GenericAPIView):
    queryset = VATPeriod.objects.all()
    serializer_class = VATPeriodSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class VATPeriodView(mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    generics.GenericAPIView):
    queryset = VATPeriod.objects.all()
    serializer_class = VATPeriodSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

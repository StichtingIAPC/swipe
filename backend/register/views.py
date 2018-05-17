from decimal import Decimal

import json
from django.db.models import F
from django.db.models import Prefetch, Count
from django.http import Http404, HttpResponseBadRequest, HttpResponse
from rest_framework import mixins, generics

from money.models import Denomination
from register.helpers import RegisterDictParsers
from register.models import RegisterMaster, Register, DenominationCount, SalesPeriod, RegisterCount, \
 PaymentType, AlreadyOpenError, RegisterCountError
from money.serializers import DenominationSerializer
from register.serializers import RegisterSerializer, PaymentTypeSerializer, \
    RegisterCountSerializer, SalesPeriodSerializer
from tools.json_parsers import ParseError, DictParsers
from www.models import SwipeLoginRequired


class RegisterListView(SwipeLoginRequired, mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):
    queryset = Register.objects.select_related(
        'payment_type'
    ).annotate(
        Count('registercount')
    ).prefetch_related(
                Prefetch(
                    'registercount_set',
                    queryset=RegisterCount.objects.filter(
                        sales_period__endTime__isnull=F('is_opening_count')
                    ).prefetch_related(
                        Prefetch(
                            'denominationcount_set',
                            queryset=DenominationCount.objects.select_related(
                                'denomination'
                            )
                        )
                    )
                )
    ).prefetch_related(
        'currency__denomination_set'
    )  # Heavy prefetch query to optimize loading of objects, and prevent optional O(n) behaviour on the DB
    serializer_class = RegisterSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RegisterOpenedView(SwipeLoginRequired, mixins.ListModelMixin,
                         generics.GenericAPIView):
    serializer_class = RegisterCountSerializer
    queryset = RegisterCount.objects\
        .filter(sales_period__endTime__isnull=True,
                is_opening_count=True,
                register__is_active=True)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RegisterClosedView(SwipeLoginRequired, mixins.ListModelMixin,
                         generics.GenericAPIView):
    serializer_class = RegisterCountSerializer

    def get_queryset(self):
        return RegisterMaster.get_last_closed_register_counts()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RegisterView(SwipeLoginRequired, mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   generics.GenericAPIView):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class PaymentTypeListView(SwipeLoginRequired, mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          generics.GenericAPIView):
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PaymentTypeView(SwipeLoginRequired, mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      generics.GenericAPIView):
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class RegisterCountListView(SwipeLoginRequired, mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            generics.GenericAPIView):
    queryset = RegisterCount.objects.prefetch_related(
        'denominationcount_set__denomination'
    ).prefetch_related(
        'register__currency__denomination_set'
    )
    serializer_class = RegisterCountSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # TODO: insert register count check/validation on creation.
        return self.create(request, *args, **kwargs)


class RegisterCountView(SwipeLoginRequired, mixins.RetrieveModelMixin,
                        generics.GenericAPIView):
    queryset = RegisterCount.objects.all()
    serializer_class = RegisterCountSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class RegisterOpenView(SwipeLoginRequired, mixins.RetrieveModelMixin,
                       generics.GenericAPIView):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer

    @staticmethod
    def deconstruct_post_body(body: dict):
        memo = DictParsers.string_parser(body.get("memo", None))
        amount = DictParsers.decimal_parser(body.get("amount", None))
        denoms = DictParsers.list_parser(body.get("denoms", None))
        denominations = []
        for denom in denoms:
            denominations.append(RegisterDictParsers.denominationcount_parser(denom))
        params = type('', (), {})
        params.memo = memo
        params.amount = amount
        params.denoms = denominations
        return params

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        try:
            register = Register.objects.get(pk=pk)
        except Register.DoesNotExist:
            raise Http404
        json_data = request.data  #type: dict
        try:
            parsed_data = RegisterOpenView.deconstruct_post_body(json_data)
        except ParseError as e:
            return HttpResponseBadRequest(reason=str(e))

        if not register.is_cash_register:
            # We can ignore the denomination counts and use the counted amount
            try:
                count = register.open(counted_amount=parsed_data.amount, memo=parsed_data.memo)
                ser = RegisterCountSerializer().to_representation(count)
                return HttpResponse(content=json.dumps(ser),
                                    content_type="application/json")
            except AlreadyOpenError:
                respo = HttpResponseBadRequest(reason="Register is already opened")
                return respo
        else:
            try:
                reg_count = register.open(counted_amount=parsed_data.amount,
                                          memo=parsed_data.memo, denominations=parsed_data.denoms)
                ser = RegisterCountSerializer().to_representation(reg_count)
                return HttpResponse(content=json.dumps(ser),
                                    content_type="application/json")
            except AlreadyOpenError:
                respo = HttpResponseBadRequest(reason="Register is already opened")
                return respo
            except RegisterCountError:
                respo = HttpResponseBadRequest(reason="Counts did not add up")
                return respo


class SalesPeriodCloseView(SwipeLoginRequired, mixins.RetrieveModelMixin,
                           generics.GenericAPIView):
    queryset = SalesPeriod.objects.all()
    serializer_class = SalesPeriodSerializer

    @staticmethod
    def deconstruct_post_body(body: dict):
        register_data = DictParsers.list_parser(body.get("register_infos"))
        counts_and_denom_counts = []

        for datum in register_data:
            register = RegisterDictParsers.register_parser(datum.get("register", None))
            amount = DictParsers.decimal_parser(datum.get("amount", None))
            reg_count = RegisterCount(register=register, amount=amount)
            denom_counts = []
            denoms = DictParsers.list_parser(datum.get("denoms", None))
            for denom in denoms:
                denom_count = RegisterDictParsers.denominationcount_parser(denom)
                denom_count.register_count = reg_count
                denom_counts.append(denom_count)
            counts_and_denom_counts.append((reg_count, denom_counts))

        params = type('', (), {})
        params.memo = body.get("memo", "")

        params.registercounts_denominationcounts = counts_and_denom_counts
        return params

    def post(self, request):
        sales_period = RegisterMaster.get_open_sales_period()
        if not sales_period:
            return HttpResponseBadRequest(reason="Salesperiod is closed")

        json_data = request.data  # type: dict
        try:
            params = SalesPeriodCloseView.deconstruct_post_body(json_data)
        except ParseError as e:
            return HttpResponseBadRequest(reason=str(e))

        period = sales_period.close(params.registercounts_denominationcounts, params.memo)
        return HttpResponse(content=json.dumps(SalesPeriodSerializer().to_representation(period)),
                            content_type="application/json")


class SalesPeriodListView(SwipeLoginRequired, mixins.ListModelMixin,
                          generics.GenericAPIView):
    queryset = SalesPeriod.objects.all()
    serializer_class = SalesPeriodSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PaymentTypeOpenListView(SwipeLoginRequired, mixins.ListModelMixin,
                              generics.GenericAPIView):
    serializer_class = PaymentTypeSerializer

    def get_queryset(self):
        return RegisterMaster.get_payment_types_for_open_registers()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SalesPeriodView(SwipeLoginRequired, mixins.RetrieveModelMixin,
                      generics.GenericAPIView):
    queryset = SalesPeriod.objects.all()
    serializer_class = SalesPeriodSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class SalesPeriodLatestView(SwipeLoginRequired, mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            generics.GenericAPIView):
    serializer_class = SalesPeriodSerializer

    def get_queryset(self):
        if SalesPeriod.objects.exists():
            return [SalesPeriod.objects.latest('beginTime')]
        else:
            return SalesPeriod.objects.none()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class LastCountView(SwipeLoginRequired, mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            generics.GenericAPIView):
    serializer_class = RegisterCountSerializer

    def get_queryset(self):
        return RegisterMaster.get_last_register_counts()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
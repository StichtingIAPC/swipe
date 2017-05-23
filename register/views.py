from decimal import Decimal

import json
from django.db.models import F
from django.db.models import Prefetch, Count
from django.http import Http404, HttpResponseBadRequest, HttpResponse
from rest_framework import mixins, generics

from money.models import Denomination
from register.models import RegisterMaster, Register, DenominationCount, SalesPeriod, RegisterCount, \
 PaymentType, AlreadyOpenError, RegisterCountError
from register.serializers import RegisterSerializer, PaymentTypeSerializer, \
    RegisterCountSerializer, SalesPeriodSerializer, DenominationSerializer

class DictParsers:

    @staticmethod
    def decimal_parser(string: str):
        if string is None:
            raise ParseError("String does not exist")
        try:
            float(string)
        except ValueError:
            raise ParseError("String is not a valid decimal")
        return Decimal(string)

    @staticmethod
    def string_parser(string: str):
        if string is None:
            raise ParseError("String does not exist")
        return string

    @staticmethod
    def denominationcount_parser(dictionary: dict):
        count = dictionary.get("count", None)
        if count is None:
            raise ParseError("Count is missing")
        if not type(count) == int:
            raise ParseError("Count is not an int")
        denomination = dictionary.get("denomination", None)
        if denomination is None:
            raise ParseError("Denomination is missing")
        if not type(denomination) == int:
            raise ParseError("Denomination is not an int")
        db_denom = Denomination.objects.get(id=denomination)
        return DenominationCount(denomination=db_denom, number=count)

    @staticmethod
    def register_parser(integer: int):
        if integer is None:
            raise ParseError("Register does not exist")
        if not type(integer) == int:
            raise ParseError("Register is not an int")
        return Register.objects.get(id=integer)

    @staticmethod
    def list_parser(obj: str):
        if obj is None:
            raise ParseError("List is missing")
        if not isinstance(obj, list):
            raise ParseError("Object is not a list")


class RegisterListView(mixins.ListModelMixin,
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


class RegisterOpenedView(mixins.ListModelMixin,
                       generics.GenericAPIView):
    serializer_class = RegisterCountSerializer
    queryset = RegisterCount.objects\
        .filter(sales_period__endTime__isnull=True,
                is_opening_count=True,
                register__is_active=True)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pass
        #obj = RegisterOpenSerializer(request.data)
        #obj.is_valid(raise_exception=True)
        #counts = obj.validated_data['counts']

        #return Response(obj)


class RegisterClosedView(mixins.ListModelMixin,
                        generics.GenericAPIView):
    serializer_class = RegisterCountSerializer

    def get_queryset(self):
        return RegisterMaster.get_last_closed_register_counts()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RegisterView(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   generics.GenericAPIView):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class PaymentTypeListView(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          generics.GenericAPIView):
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PaymentTypeView(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      generics.GenericAPIView):
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class RegisterCountListView(mixins.ListModelMixin,
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


class RegisterCountView(mixins.RetrieveModelMixin,
                        generics.GenericAPIView):
    queryset = RegisterCount.objects.all()
    serializer_class = RegisterCountSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class RegisterOpenView(mixins.RetrieveModelMixin,
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
            denominations.append(DictParsers.denominationcount_parser(denom))
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


class SalesPeriodCloseView(mixins.RetrieveModelMixin,
                           generics.GenericAPIView):
    queryset = SalesPeriod.objects.all()
    serializer_class = SalesPeriodSerializer

    @staticmethod
    def deconstruct_post_body(body: dict):
        register_data = DictParsers.list_parser(body.get("register_infos", None))
        counts_and_denom_counts = []

        for datum in register_data:
            register = DictParsers.register_parser(datum.get("register", None))
            amount = DictParsers.decimal_parser(datum.get("amount", None))
            reg_count = RegisterCount(register=register, amount=amount)
            denom_counts = []
            denoms = DictParsers.list_parser(datum.get("denoms", None))
            for denom in denoms:
                denom_count = DictParsers.denominationcount_parser(denom)
                denom_counts.register_count = reg_count
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


class SalesPeriodListView(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          generics.GenericAPIView):
    queryset = SalesPeriod.objects.all()
    serializer_class = SalesPeriodSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SalesPeriodView(mixins.RetrieveModelMixin,
                      generics.GenericAPIView):
    queryset = SalesPeriod.objects.all()
    serializer_class = SalesPeriodSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class SalesPeriodLatestView(mixins.ListModelMixin,
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


class DenominationListView(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = DenominationSerializer
    queryset = Denomination.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ParseError(Exception):
    pass

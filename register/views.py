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
    RegisterCountSerializer, SalesPeriodSerializer


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
    
    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        try:
            register = Register.objects.get(pk=pk)
        except Register.DoesNotExist:
            raise Http404
        json_data=request.data  #type: dict
        memo = json_data.get("memo", None)
        if memo is None:
            respo = HttpResponseBadRequest(reason="Memo is missing")
            return respo
        amount = json_data.get("amount", None) # type: str
        if amount is None:
            respo = HttpResponseBadRequest(reason="Amount is missing")
            return respo
        try:
            float(amount)
        except ValueError:
            respo = HttpResponseBadRequest(reason="Amount is malformed")
            return respo
        counted_amount = Decimal(amount)
        denoms = json_data.get("denoms", None)
        if denoms is None:
            respo = HttpResponseBadRequest(reason="Denominationcounts are missing")
            return respo
        if not isinstance(denoms, list):
            respo = HttpResponseBadRequest(reason="Denominationcounts are malformed")
            return respo
        if not register.is_cash_register:
            # We can ignore the denomination counts and use the counted amount
            try:
                count = register.open(counted_amount=counted_amount, memo=memo)
                ser = RegisterCountSerializer().to_representation(count)
                return HttpResponse(content=json.dumps(ser),
                                    content_type="application/json")
            except AlreadyOpenError:
                respo = HttpResponseBadRequest(reason="Register is already opened")
                return respo
        else:
            # We need to get denominations from the database to create our own denomination counts
            # If the counts don't match, return an error
            db_denoms = Denomination.objects.filter(currency=register.currency)
            denom_dict = {}
            for denom in db_denoms:
                denom_dict[denom.amount] = denom

            denomination_counts = []
            for json_denom in denoms:
                count = json_denom["count"]
                amount = json_denom["amount"]
                try:
                    float(amount)
                except ValueError:
                    respo = HttpResponseBadRequest(reason="Denominationcounts are malformed")
                    return respo
                if not count.isnumeric():
                    respo = HttpResponseBadRequest(reason="Denominationcounts are malformed")
                    return respo
                decimal_value = Decimal(amount)
                count_int = int(count)
                db_denom = denom_dict.get(decimal_value, None)
                if db_denom is None:
                    respo = HttpResponseBadRequest(reason="Denominationcounts is of non-existent denomination")
                    return respo
                denomination_counts.append(DenominationCount(denomination=db_denom, number=count_int))

            try:
                reg_count = register.open(counted_amount=counted_amount, memo=memo, denominations=denomination_counts)
                ser=RegisterCountSerializer().to_representation(reg_count)
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
        register_data = body.get("register_infos", None)
        if register_data is None:
            raise ParseError("No register_data available")
        counts_and_denom_counts = []

        for datum in register_data:
            register = datum.get("register", None)
            if register is None:
                raise ParseError("Register is missing")
            try:
                register = int(register)
            except Exception:
                raise ParseError("Register is not a number")
            register = Register.objects.get(id=register)
            amount = datum.get("amount", None)
            if amount is None:
                raise ParseError("Amount is missing")
            try:
                float(amount)
            except Exception:
                raise ParseError("Amount is not decimal")
            amount = Decimal(amount)
            reg_count = RegisterCount(register=register, amount=amount)
            denom_counts = []
            denoms = datum.get("denoms", None)
            if denoms is None:
                raise ParseError("Denoms are missing")
            if not isinstance(denoms, list):
                raise ParseError("Denoms is not a list")
            for denom in denoms:
                count = denom.get("count", None)
                denomination = denom.get("denomination", None)
                try:
                    int(denomination)
                except ValueError:
                    raise ParseError("Denomination is not a number")
                db_denom = Denomination.objects.get(id=denomination)
                try:
                    count = int(count)
                except Exception:
                    raise ParseError("Denominationcounts are malformed")
                denom_counts.append(DenominationCount(register_count=reg_count,
                                                      denomination=db_denom,
                                                      number=count))
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


class ParseError(Exception):
    pass

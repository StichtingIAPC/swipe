from rest_framework import generics
from rest_framework import mixins
from django.http import Http404, HttpResponseBadRequest, HttpResponse, JsonResponse
from django.db.models import Sum
import json

from article.helpers import ArticleDictParsers
from crm.helpers import CRMDictParsers
from money.serializers import MoneySerializerField
from money.helpers import MoneyDictParsers
from register.views import ParseError
from sales.helpers import SalesDictParsers
from sales.models import Payment, Transaction, TransactionLine, SalesTransactionLine, OtherCostTransactionLine, \
    OtherTransactionLine, RefundTransactionLine
from sales.serializers import PaymentSerializer, TransactionSerializer
from register.models import RegisterMaster, SalesPeriod
from tools.json_parsers import DictParsers


class PaymentListView(mixins.ListModelMixin,
                      generics.GenericAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PaymentGroupView(mixins.RetrieveModelMixin,
                       generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        self.queryset = Payment.objects.filter(transaction__salesperiod__id=kwargs["pk"]).order_by("payment_type")
        resultset = []
        type_list = []
        first_of_type = True
        current_type = None
        for element in self.queryset:
            if first_of_type:
                type_list = []
                current_type = element.payment_type
                first_of_type = False
            if current_type == element.payment_type:
                type_list.append(PaymentSerializer().to_representation(element))
            else:
                first_of_type=True
                resultset.append(type_list)
        resultset.append(type_list)
        return HttpResponse(content = json.dumps(resultset, indent=4), content_type="application/json")


class PaymentGroupOpenedView(mixins.RetrieveModelMixin,
                             generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        self.queryset = Payment.objects.filter(transaction__salesperiod__endTime=None).order_by("payment_type")
        resultset = []
        type_list = []
        first_of_type = True
        current_type = None
        for element in self.queryset:
            if first_of_type:
                type_list = []
                current_type = element.payment_type
                first_of_type = False
            if current_type == element.payment_type:
                type_list.append(PaymentSerializer().to_representation(element))
            else:
                first_of_type=True
                resultset.append(type_list)
        resultset.append(type_list)
        return HttpResponse(content = json.dumps(resultset, indent=4), content_type="application/json")


class PaymentOpenListView(mixins.ListModelMixin,
                          generics.GenericAPIView):
    serializer_class = PaymentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        if not RegisterMaster.sales_period_is_open():
            return Payment.objects.none()
        else:
            opensalesperiod = RegisterMaster.get_open_sales_period()
            return Payment.objects.filter(transaction__salesperiod=opensalesperiod)


class PaymentView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class TransactionView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class TransactionListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class TransactionOpenView(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(salesperiod__endTime__isnull=True)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PaymentTotalsView(generics.GenericAPIView, mixins.ListModelMixin):

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        # This can most likely be done much more efficiently than iteration, Django is not very clear about it
        payments = Payment.objects.filter(transaction__salesperiod__id=pk)
        serialization = PaymentTotalsView.get_aggregation_and_serialize(payments)
        return HttpResponse(content=json.dumps(serialization), content_type="application/json")

    @staticmethod
    def get_aggregation_and_serialize(payments):
        payment_type_aggregation = {}
        for payment in payments:
            total = payment_type_aggregation.get((payment.payment_type_id, payment.amount.currency.iso))
            if total:
                payment_type_aggregation[
                    (payment.payment_type_id, payment.amount.currency.iso)] = total + payment.amount
            else:
                payment_type_aggregation[(payment.payment_type_id, payment.amount.currency.iso)] = payment.amount
        serialization = []
        for key in payment_type_aggregation:
            serialization.append({'paymenttype': key[0],
                                  'amount': MoneySerializerField().to_representation(payment_type_aggregation[key])})
        return serialization


class PaymentsLatestTotalsView(generics.GenericAPIView, mixins.ListModelMixin):

    def get(self, request, *args, **kwargs):
        sp = SalesPeriod.objects.all().latest('beginTime')
        payments = Payment.objects.filter(transaction__salesperiod=sp)
        serialization = PaymentTotalsView.get_aggregation_and_serialize(payments)
        return HttpResponse(content=json.dumps(serialization, indent=4), content_type="application/json")


class TransactionCreateView(generics.GenericAPIView, mixins.RetrieveModelMixin):

    @staticmethod
    def deconstruct_post_body(body):
        user = CRMDictParsers.user_parser(body.get("user"))
        print("HERE")
        # Customer is Optional
        customer_int = body.get("customer", None)
        if customer_int:
            customer = CRMDictParsers.customer_parser(customer_int)
        else:
            customer = None
        payments = DictParsers.list_parser(body.get("payments"))
        payment_list = []
        for payment in payments:
            print(payment)
            payment_list.append(SalesDictParsers.payment_parser(payment))
        print("HER!E")

        transactionlines = DictParsers.list_parser(body.get("transactionlines"))
        transaction_list = []
        print("HER!E")
        for line in transactionlines:
            transaction_list.append(SalesDictParsers.transactionline_parser(line))
        print("There")
        data = type('', (), {})
        data.user = user
        data.customer = customer
        data.transaction_lines = transaction_list
        data.payments = payment_list
        return data

    def post(self, request, *args, **kwargs):
        json_data = request.data # type: dict
        try:
            data = TransactionCreateView.deconstruct_post_body(json_data)
        except ParseError as e:
            return HttpResponseBadRequest(reason=str(e))
        try:
            transaction = Transaction.create_transaction(user=data.user, payments=data.payments,
                                                         transaction_lines=data.transaction_lines,
                                                         customer=data.customer)
        except Exception as e:
            return HttpResponseBadRequest(reason=str(e))
        return HttpResponse(content=json.dumps(TransactionSerializer().to_representation(transaction), indent=4),
                            content_type='application/json')

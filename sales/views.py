from rest_framework import generics
from rest_framework import mixins

from sales.models import Payment, Transaction, TransactionLine
from sales.serializers import PaymentSerializer, TransactionSerializer
from register.models import RegisterMaster


class PaymentListView(mixins.ListModelMixin,
                          generics.GenericAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PaymentOpenListView(mixins.ListModelMixin,
                          generics.GenericAPIView):
    serializer_class = PaymentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        if (not RegisterMaster.sales_period_is_open()):
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
from rest_framework import generics
from rest_framework import mixins

from sales.models import Payment
from sales.serializers import PaymentSerializer


class PaymentListView(mixins.ListModelMixin,
                          generics.GenericAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


from rest_framework import generics
from rest_framework import mixins

from crm.models import Customer
from crm.serializers import CustomerSerializer


class CustomerView(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      generics.GenericAPIView):

    def get_queryset(self):
        return Customer.objects.all()

    serializer_class = CustomerSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
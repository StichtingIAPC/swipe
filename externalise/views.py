from django.shortcuts import render
from rest_framework import mixins, generics
from externalise.models import ExternaliseDocument
from externalise.serializers import ExternaliseDocumentSerializer


class ExternaliseDocumentView(mixins.RetrieveModelMixin,
                      generics.GenericAPIView):
    queryset = ExternaliseDocument.objects.all()
    serializer_class = ExternaliseDocumentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ExternaliseDocumentListView(mixins.ListModelMixin,
                      generics.GenericAPIView):
    queryset = ExternaliseDocument.objects.all()
    serializer_class = ExternaliseDocumentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
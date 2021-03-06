from rest_framework import generics
from rest_framework import mixins

from assortment.models import AssortmentUnitType, AssortmentLabelType
from assortment.serializers import UnitTypeSerializer, LabelTypeSerializer, LabelTypeSerializerWithEdit, \
    UnitTypeSerializerWithEdit
from www.models import SwipeLoginRequired


class UnitTypeListView(SwipeLoginRequired, mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):
    queryset = AssortmentUnitType.objects.all()
    serializer_class = UnitTypeSerializerWithEdit

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UnitTypeDetailView(SwipeLoginRequired, mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         generics.GenericAPIView):
    queryset = AssortmentUnitType.objects.all()
    serializer_class = UnitTypeSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class LabelTypeListView(SwipeLoginRequired, mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        generics.GenericAPIView):
    queryset = AssortmentLabelType.objects.all()
    serializer_class = LabelTypeSerializerWithEdit

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class LabelTypeDetailView(SwipeLoginRequired, mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          generics.GenericAPIView):
    queryset = AssortmentLabelType.objects.all()
    serializer_class = LabelTypeSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

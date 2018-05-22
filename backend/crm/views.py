from django.http import HttpRequest
from django.http import HttpResponse
from rest_framework import generics
from rest_framework import mixins

from crm.models import Customer, Person, Organisation, ContactOrganisation
from crm.serializers import CustomerSerializer, PersonSerializer, OrganisationSerializer, \
    DetailedContactOrganisationSerializer, \
    ContactOrganisationSerializer
from www.models import SwipeLoginRequired


class CustomerView(SwipeLoginRequired, mixins.RetrieveModelMixin,
                   generics.GenericAPIView):

    def get_queryset(self):
        return Customer.objects.all()

    serializer_class = CustomerSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        Customer.objects.filter(id=kwargs['pk']).delete()
        return HttpResponse(content={'deleted': True}, status=200)

class CustomerListView(SwipeLoginRequired, mixins.ListModelMixin,
                   generics.GenericAPIView):

    def get_queryset(self):
        return Customer.objects.all()

    serializer_class = CustomerSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PersonView(SwipeLoginRequired, mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.CreateModelMixin,
                 generics.GenericAPIView):

    def get_queryset(self):
        return Person.objects.all()

    serializer_class = PersonSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        Person.objects.filter(id=kwargs['pk']).delete()
        return HttpResponse(content={'deleted': True}, status=200)


class PersonCreateView(SwipeLoginRequired, mixins.CreateModelMixin,
                       generics.GenericAPIView):
    serializer_class = PersonSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class OrganisationView(SwipeLoginRequired, mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):

    def get_queryset(self):
        return Organisation.objects.all()

    serializer_class = OrganisationSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        Organisation.objects.filter(id=kwargs['pk']).delete()
        return HttpResponse(content={'deleted': True}, status=200)


class OrganisationCreateView(SwipeLoginRequired, mixins.CreateModelMixin,
                             generics.GenericAPIView):
    serializer_class = OrganisationSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ContactOrganisationView(SwipeLoginRequired, mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.CreateModelMixin,
                              generics.GenericAPIView):

    def get_queryset(self):
        return ContactOrganisation.objects.all()

    def get(self, request, *args, **kwargs):
        self.serializer_class = DetailedContactOrganisationSerializer
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        self.serializer_class = ContactOrganisationSerializer
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        ContactOrganisation.objects.filter(id=kwargs['pk']).delete()
        return HttpResponse(content={'deleted': True}, status=200)


class ContactOrganisationCreateView(SwipeLoginRequired, mixins.CreateModelMixin,
                                    generics.GenericAPIView):
    serializer_class = ContactOrganisationSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

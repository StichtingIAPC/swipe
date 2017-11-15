from rest_framework import generics
from rest_framework import mixins

from crm.models import Customer, Person, Organisation, ContactOrganisation
from crm.serializers import CustomerSerializer, PersonSerializer, OrganisationSerializer, DetailedContactOrganisationSerializer, \
    ContactOrganisationSerializer


class CustomerView(mixins.RetrieveModelMixin,
                      generics.GenericAPIView):

    def get_queryset(self):
        return Customer.objects.all()

    serializer_class = CustomerSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class PersonView(mixins.RetrieveModelMixin,
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

    # TODO: Implement delete


class PersonCreateView(mixins.CreateModelMixin,
                       generics.GenericAPIView):

    serializer_class = PersonSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class OrganisationView(mixins.RetrieveModelMixin,
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

    # TODO: Implement delete

class OrganisationCreateView(mixins.CreateModelMixin,
                       generics.GenericAPIView):

    serializer_class = OrganisationSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ContactOrganisationView(mixins.RetrieveModelMixin,
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

    # TODO: Implement delete


class ContactOrganisationCreateView(mixins.CreateModelMixin,
                       generics.GenericAPIView):

    serializer_class = ContactOrganisationSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


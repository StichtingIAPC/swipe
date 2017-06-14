from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.forms import Form
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View

from crm.models import Customer, ContactOrganisation,\
    Person, PersonType, PersonTypeField, PersonTypeFieldValue,\
    Organisation, OrganisationType, OrganisationTypeField, OrganisationTypeFieldValue, User
from tools.json_parsers import ParseError


def index(request):
    return render(request, 'crm/index.html')


class CRMDictParsers:

    @staticmethod
    def user_parser(integer: int):
        if integer is None:
            raise ParseError("User does not exist")
        if not isinstance(integer, int):
            raise ParseError("User id is not integer")
        return User.objects.get(id=integer)

    @staticmethod
    def customer_parser(integer: int):
        if integer is None:
            raise ParseError("Customer does not exist")
        if not isinstance(integer, int):
            raise ParseError("Customer id is not integer")
        return Customer.objects.get(id=integer)

###
# Customer related views
###
class CustomerList(LoginRequiredMixin, ListView):
    model = Customer

    def get_context_data(self, **kwargs):
        context = super(CustomerList, self).get_context_data()
        return context


class CustomerDetail(LoginRequiredMixin, DetailView):
    model = Customer

    def get_context_data(self, **kwargs):
        context = super(CustomerDetail, self).get_context_data()

        if hasattr(self.object, 'person'):
            context['values'] = self.object.person
        elif hasattr(self.object, 'contactorganisation'):
            context['values'] = self.object.contactorganisation.organisation
        else:
            context['values'] = self.object

        context['object'] = self.object

        # Add the typefields for the customer to the context
        if hasattr(self.object, 'person'):
            context['types'] = self.object.person.get_type_fields()
        elif hasattr(self.object, 'contactorganisation'):
            context['types'] = self.object.contactorganisation.organisation.get_type_fields()
            context['contact_types'] = self.object.contactorganisation.contact.get_type_fields()
        else:
            context['types'] = []

        return context


class CustomerDelete(PermissionRequiredMixin, DeleteView):
    model = Customer
    permission_required = 'customer.delete_customer'
    success_url = reverse_lazy('customer_list')


###
# Person related views
###
class PersonCreate(PermissionRequiredMixin, CreateView):
    model = Person
    template_name = 'crm/customer_form.html'
    permission_required = 'customer.add_customer'
    fields = ['name', 'email', 'address', 'zip_code', 'city', 'phone', 'memo', 'types']
    success_url = reverse_lazy('customer_list')


class PersonEdit(PermissionRequiredMixin, UpdateView):
    model = Person
    template_name = 'crm/customer_form.html'
    permission_required = 'customer.change_customer'
    fields = ['name', 'email', 'address', 'zip_code', 'city', 'phone', 'memo', 'types']
    success_url = reverse_lazy('customer_list')

    def get_context_data(self, **kwargs):
        context = super(PersonEdit, self).get_context_data()
        context['object'] = self.object
        return context


###
# Organisation related views
###
class OrganisationCreate(PermissionRequiredMixin, CreateView):
    model = Organisation
    template_name = 'crm/customer_form.html'
    permission_required = 'customer.add_customer'
    fields = ['name', 'email', 'address', 'zip_code', 'city', 'phone', 'fax', 'kvk', 'memo',
              'parent_organisation', 'types']
    success_url = reverse_lazy('customer_list')


class OrganisationEdit(PermissionRequiredMixin, UpdateView):
    model = Organisation
    template_name = 'crm/customer_form.html'
    permission_required = 'customer.change_customer'
    fields = ['name', 'email', 'address', 'zip_code', 'city', 'phone', 'fax', 'kvk', 'memo',
              'parent_organisation', 'types']
    success_url = reverse_lazy('customer_list')

    def get_context_data(self, **kwargs):
        context = super(OrganisationEdit, self).get_context_data()
        context['object'] = self.object
        return context


###
# ContactOrganisation related views
###
class ContactOrganisationCreate(PermissionRequiredMixin, CreateView):
    model = ContactOrganisation
    template_name = 'crm/contactorganisation_form.html'
    permission_required = 'contactorganisation.add_contactorganisation'
    fields = ['contact', 'organisation']
    success_url = reverse_lazy('customer_list')


class ContactOrganisationEdit(PermissionRequiredMixin, UpdateView):
    model = ContactOrganisation
    template_name = 'crm/customer_form.html'
    permission_required = 'customer.change_customer'
    fields = ['contact', 'organisation']
    success_url = reverse_lazy('customer_list')

    def get_context_data(self, **kwargs):
        context = super(ContactOrganisationEdit, self).get_context_data()
        context['object'] = self.object
        return context


###
# View to save a customer's type fields
###
class TypeFieldSave(PermissionRequiredMixin, View):
    permission_required = 'customer.change_customer'
    formfield_prefix = "typefield"

    def post(self, request, object_type, pk):
        # Check if the form meets basic validations
        if Form(request.POST).is_valid():
            print(request.POST)
            typefields = [f for f in request.POST.keys() if f.startswith(self.formfield_prefix)]

            # Determine which type of object we need
            if object_type == "organisation":
                object_type = Organisation
                object_types_type = OrganisationType
                object_type_fields_type = OrganisationTypeField
                object_type_field_values_type = OrganisationTypeFieldValue
            elif object_type == "person":
                object_type = Person
                object_types_type = PersonType
                object_type_fields_type = PersonTypeField
                object_type_field_values_type = PersonTypeFieldValue
            else:
                raise TypeError("The object type {} has no support for typefields.".format(object_type))

            # Get the object of which we need to edit the fields
            obj = get_object_or_404(object_type, pk=pk)
            obj_fields = obj.get_type_fields()

            # Parse the typefieldvalues are in the form
            for form_field_name in typefields:
                try:
                    _, c_type_id, field_id = form_field_name.split("_")
                except ValueError as e:
                    raise ValueError("Form field name does not match expected pattern; {}".format(e))

                if c_type_id == "" or field_id == "":
                    raise ValueError("Form field name does not match expected pattern.")

                # Get the types this object has
                obj_type = object_types_type.objects.get(pk=int(c_type_id))
                obj_type_field = object_type_fields_type.objects.get(pk=int(field_id))

                object_field = obj_fields[int(c_type_id)]['fields'][int(field_id)]

                # If the field does not have a value yet, create one
                if not isinstance(object_field['value'], object_type_field_values_type):

                    object_field['value'] = object_type_field_values_type.objects.create(
                        value=request.POST[form_field_name],
                        typefield=obj_type_field,
                        type=obj_type,
                        object=obj)

                # If the value changed, update the field.
                if request.POST[form_field_name] != object_field['value'].value:
                    object_field['value'].value = request.POST[form_field_name]
                    object_field['value'].save()

            if object_type == "organisation":
                return redirect(to="customer_edit_organisation", pk=pk)
            elif object_type == "person":
                return redirect(to="customer_edit_person", pk=pk)
            else:
                return redirect(to="customer_list")

        else:
            return HttpResponseBadRequest("<h1>Bad request</h1><p>The form was not valid.</p>")


###
# PersonType related views
###
class PersonTypeList(LoginRequiredMixin, ListView):
    model = PersonType


class PersonTypeDetail(LoginRequiredMixin, DetailView):
    model = PersonType


class PersonTypeDelete(PermissionRequiredMixin, DeleteView):
    model = PersonType
    permission_required = 'persontype.delete_persontype'
    success_url = reverse_lazy('persontype_list')


class PersonTypeCreate(PermissionRequiredMixin, CreateView):
    model = PersonType
    permission_required = 'persontype.add_persontype'
    fields = ['name', 'typefields']
    success_url = reverse_lazy('persontype_list')


class PersonTypeEdit(PermissionRequiredMixin, UpdateView):
    model = PersonType
    permission_required = 'persontype.change_persontype'
    fields = ['name', 'typefields']
    success_url = reverse_lazy('persontype_list')


###
# OrganisationType related views
###
class OrganisationTypeList(LoginRequiredMixin, ListView):
    model = OrganisationType


class OrganisationTypeDetail(LoginRequiredMixin, DetailView):
    model = OrganisationType


class OrganisationTypeDelete(PermissionRequiredMixin, DeleteView):
    model = OrganisationType
    permission_required = 'organisationtype.delete_organisationtype'
    success_url = reverse_lazy('organisationtype_list')


class OrganisationTypeCreate(PermissionRequiredMixin, CreateView):
    model = OrganisationType
    permission_required = 'organisationtype.add_organisationtype'
    fields = ['name', 'typefields']
    success_url = reverse_lazy('organisationtype_list')


class OrganisationTypeEdit(PermissionRequiredMixin, UpdateView):
    model = OrganisationType
    permission_required = 'organisationtype.change_organisationtype'
    fields = ['name', 'typefields']
    success_url = reverse_lazy('organisationtype_list')


###
# PersonTypeField related views
###
class PersonTypeFieldList(LoginRequiredMixin, ListView):
    model = PersonTypeField
    template_name = 'crm/typefield_list.html'


class PersonTypeFieldDetail(LoginRequiredMixin, DetailView):
    model = PersonTypeField
    template_name = 'crm/typefield_detail.html'


class PersonTypeFieldDelete(PermissionRequiredMixin, DeleteView):
    model = PersonTypeField
    permission_required = 'persontypefield.delete_persontypefield'
    success_url = reverse_lazy('persontypefield_list')
    template_name = 'crm/typefield_confirm_delete.html'


class PersonTypeFieldCreate(PermissionRequiredMixin, CreateView):
    model = PersonTypeField
    permission_required = 'persontypefield.add_persontypefield'
    fields = ['name']
    success_url = reverse_lazy('persontypefield_list')
    template_name = 'crm/typefield_form.html'


class PersonTypeFieldEdit(PermissionRequiredMixin, UpdateView):
    model = PersonTypeField
    permission_required = 'persontypefield.change_persontypefield'
    fields = ['name']
    success_url = reverse_lazy('persontypefield_list')
    template_name = 'crm/typefield_form.html'


###
# TypeField related views
###
class OrganisationTypeFieldList(LoginRequiredMixin, ListView):
    model = OrganisationTypeField
    template_name = 'crm/typefield_list.html'


class OrganisationTypeFieldDetail(LoginRequiredMixin, DetailView):
    model = OrganisationTypeField
    template_name = 'crm/typefield_detail.html'


class OrganisationTypeFieldDelete(PermissionRequiredMixin, DeleteView):
    model = OrganisationTypeField
    permission_required = 'organisationtypefield.delete_organisationtypefield'
    success_url = reverse_lazy('organisationtypefield_list')
    template_name = 'crm/typefield_confirm_delete.html'


class OrganisationTypeFieldCreate(PermissionRequiredMixin, CreateView):
    model = OrganisationTypeField
    permission_required = 'organisationtypefield.add_organisationtypefield'
    fields = ['name']
    success_url = reverse_lazy('organisationtypefield_list')
    template_name = 'crm/typefield_form.html'


class OrganisationTypeFieldEdit(PermissionRequiredMixin, UpdateView):
    model = OrganisationTypeField
    permission_required = 'organisationtypefield.change_organisationtypefield'
    fields = ['name']
    success_url = reverse_lazy('organisationtypefield_list')
    template_name = 'crm/typefield_form.html'

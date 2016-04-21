from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from core.models import SoftDeletable
from crm.exceptions import CyclicParenthoodError


class Customer(SoftDeletable):
    def __str__(self):
        if hasattr(self, 'person'):
            return self.person.name
        elif hasattr(self, 'contactorganisation'):
            return "{} - {}".format(self.contactorganisation.organisation.name, self.contactorganisation.contact.name)
        else:
            return super(Customer, self).__str__()

    def save(self, **kwargs):
        # You may only create customers if it is a Person or a ContactOrganisation
        if not isinstance(self, Person) and not isinstance(self, ContactOrganisation):
            raise AttributeError("You cannot create bare Customers. "
                                 "Please create either a Person or a ContactOrganisation.")

        super(Customer, self).save()

    def verify(self):
        """
        Verify if Customer is either a person or a contactorganisation.
        :return: A tuple of (True, "", None) if this customer is consistent, (False, "Reason", self) if not.
        :rtype: tuple(bool, str, self|None)
        """
        if not hasattr(self, 'person') and not hasattr(self, 'contactorganisation'):
            return False, "Customer is not a person or contactorganisation", self

        return True, "", None


class PersonTypeField(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Field name"))

    def __str__(self):
        return self.name


class PersonTypeFieldValue(models.Model):

    class Meta:
        unique_together = ("typefield", "type", "object")

    value = models.CharField(max_length=255, verbose_name=_("Field value"))
    typefield = models.ForeignKey(to="PersonTypeField", verbose_name=_("Person type field"))
    type = models.ForeignKey(to="PersonType", verbose_name=_("Person type"))
    object = models.ForeignKey(to="Person", verbose_name=_("Person"))

    def __str__(self):
        return self.value


class PersonType(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Person type name"))
    typefields = models.ManyToManyField(PersonTypeField, blank=True, verbose_name=_("Person type fields"))

    def __str__(self):
        return self.name


class Person(Customer):
    name = models.CharField(max_length=255, verbose_name=_("Customer name"))
    email = models.EmailField(verbose_name=_("Email address"))

    address = models.CharField(max_length=255, blank=True, verbose_name=_("Address"))
    zip_code = models.CharField(max_length=255, blank=True, verbose_name=_("Zip code"))
    city = models.CharField(max_length=255, blank=True, verbose_name=_("City"))
    phone = models.CharField(max_length=255, blank=True, verbose_name=_("Phone number"))

    memo = models.TextField(blank=True, verbose_name=_("Memo"))

    types = models.ManyToManyField(PersonType, blank=True, verbose_name=_("Person types"))

    # Optional OneToOneField to link this person to a User in the system.
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_("Swipe username"))

    def verify(self):
        """
        Verify if this Person is consistent and the information is programatically correct.
        :return: A tuple of (True, "", None) if this instance is consistent, (False, "Reason", self) if not.
        :rtype: tuple(bool, str, self|None)
        """

        # A person needs a name and e-mail
        if self.name is None or self.name == "":
            return False, "A person requires a name", self

        if self.email is None or self.email == "":
            return False, "A person requires an e-mail address", self

        return True, "", None

    def __str__(self):
        return self.name

    def get_full_address(self):
        return """
            {}
            {}
            {} {}
            """.format(self.name, self.address, self.zip_code, self.city)

    @staticmethod
    def get_type():
        return "person"

    def get_type_fields(self):
        type_fields = {}

        for person_type in self.types.all():
            type_fields[person_type.pk] = {
                'type': person_type,
                'fields': {}
            }

            for type_field in person_type.typefields.all():
                type_field_values = type_field.persontypefieldvalue_set.filter(object=self)
                type_fields[person_type.pk]['fields'][type_field.pk] = {
                    'field': type_field,
                    'value': type_field_values[0] if len(type_field_values) > 0 else ""
                }

        return type_fields


class ContactOrganisation(Customer):
    contact = models.ForeignKey(to="Person", verbose_name=_("Person"))
    organisation = models.ForeignKey(to="Organisation", verbose_name=_("Organisation"))

    def verify(self):
        """
        Verify if this contactorganisation is programatically correct.
        :return: A tuple of (True, "", None) if this instance is consistent, (False, "Reason", self) if not.
        :rtype: tuple(bool, str, self|None)
        """
        if self.contact is None:
            return False, "Contactorganisation requires a contact", self

        if self.organisation is None:
            return False, "Contactorganisation requires an organisation", self

        return True, "", None


class OrganisationTypeField(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Field name"))

    def __str__(self):
        return self.name


class OrganisationTypeFieldValue(models.Model):

    class Meta:
        unique_together = ("typefield", "type", "object")

    value = models.CharField(max_length=255, verbose_name=_("Field value"))
    typefield = models.ForeignKey(to="OrganisationTypeField", verbose_name=_("Organisation type field"))
    type = models.ForeignKey(to="OrganisationType", verbose_name=_("Organisation type"))
    object = models.ForeignKey(to="Organisation", verbose_name=_("Organisation"))

    def __str__(self):
        return self.value


class OrganisationType(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Organisation type name"))
    typefields = models.ManyToManyField(OrganisationTypeField, blank=True, verbose_name=_("Organisation type fields"))

    def __str__(self):
        return self.name


class Organisation(SoftDeletable):
    # CharFields which are inherited from parent organisations
    inherited_fields = ["address", "zip_code", "city", "phone", "fax", "kvk"]

    name = models.CharField(max_length=255, verbose_name=_("Customer name"))
    email = models.EmailField(verbose_name=_("Email address"))

    address = models.CharField(max_length=255, blank=True, verbose_name=_("Address"))
    zip_code = models.CharField(max_length=255, blank=True, verbose_name=_("Zip code"))
    city = models.CharField(max_length=255, blank=True, verbose_name=_("City"))
    phone = models.CharField(max_length=255, blank=True, verbose_name=_("Phone number"))

    fax = models.CharField(max_length=255, blank=True, verbose_name=_("Fax number"))
    kvk = models.CharField(max_length=8, blank=True, verbose_name=_("KvK number"))

    memo = models.TextField(blank=True, verbose_name=_("Memo"))

    parent_organisation = models.ForeignKey(to="Organisation", blank=True, null=True,
                                            verbose_name=_("Parent organisation"))

    types = models.ManyToManyField(OrganisationType, blank=True, verbose_name=_("Organisation types"))
    
    def __init__(self, *args, **kwargs):
        super(Organisation, self).__init__(*args, **kwargs)

        # Inherit values from parent if they are not already set.
        if hasattr(self, "parent_organisation") and self.parent_organisation is not None:
            for field in self.inherited_fields:
                if getattr(self, field, "") == "":
                    setattr(self, field, getattr(self.parent_organisation, field, ""))

    def save(self, **kwargs):
        # Cycle detection for parent organisation
        if self._has_cycle():
            raise CyclicParenthoodError(self)

        # Empty the fields which are the same as the parent's fields, to avoid saving them.
        if hasattr(self, "parent_organisation") and self.parent_organisation is not None:
            for field in self.inherited_fields:
                if getattr(self, field, "") == getattr(self.parent_organisation, field, ""):
                    setattr(self, field, "")

        super(Organisation, self).save(**kwargs)

        # Re-fill the values from the parent, to make sure the object is still usable after saving.
        if hasattr(self, "parent_organisation") and self.parent_organisation is not None:
            for field in self.inherited_fields:
                if getattr(self, field, "") == "":
                    setattr(self, field, getattr(self.parent_organisation, field, ""))

    def verify(self):
        """
        Verify if this organisation is consistent and information is programatically correct.
        :return: A tuple of (True, "", None) if this organisation is consistent, (False, "Reason", Organisation) if not.
        :rtype: tuple(bool, str, Organisation)
        """

        # A name is required
        if self.name is None or self.name == "":
            return False, "Organisation has no name", self

        # An e-mail is required
        if self.email is None or self.email == "":
            return False, "Organisation has no e-mail", self

        # No cycles should be present
        if self._has_cycle():
            return False, "Cyclic parenthood detected", self

        # Everything checks out.
        return True, "", None

    def _has_cycle(self):
        """
        Cycle detection for parent_organisation tree based on the
        Turtle and Hare problem (http://www.siafoo.net/algorithm/10)
        :return: True if the parent tree contains cycles, False if not.
        :rtype: bool
        """
        tortoise = self
        hare = self

        while True:
            if hare is None:
                return False
            hare = hare.parent_organisation

            if hare is None:
                return False
            hare = hare.parent_organisation

            tortoise = tortoise.parent_organisation

            if hare == tortoise:
                return True

    def __str__(self):
        return self.name

    @staticmethod
    def get_type():
        return "organisation"

    def get_type_fields(self):
        type_fields = {}

        for organisation_type in self.types.all():
            type_fields[organisation_type.pk] = {
                'type': organisation_type,
                'fields': {}
            }

            for type_field in organisation_type.typefields.all():
                type_field_values = type_field.organisationtypefieldvalue_set.filter(object=self)
                type_fields[organisation_type.pk]['fields'][type_field.pk] = {
                    'field': type_field,
                    'value': type_field_values[0] if len(type_field_values) > 0 else ""
                }

        return type_fields

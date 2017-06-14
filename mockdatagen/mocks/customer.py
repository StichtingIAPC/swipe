from _pydecimal import Decimal

from crm.models import Customer, Person, Organisation, ContactOrganisation
from mockdatagen.helpers import register_mock_gen
from money.models import Currency, CurrencyData, Denomination
from register.models import PaymentType, Register, RegisterCount, SalesPeriod, DenominationCount, RegisterMaster


@register_mock_gen
class CustomerGen:
    model = Person

    @staticmethod
    def func():
        customer_person_1 = Person(address="Drienerlolaan 5", city="Enschede", email="bestuur@iapc.utwente.nl",
                                        name="Jaap de Steen", phone="0534893927", zip_code="7522NB")
        customer_person_1.save()
        customer_person_2 = Person(address="Drienerlolaan 5", city="Enschede",
                                        email="schaduwbestuur@iapc.utwente.nl", name="Gerda Steenhuizen",
                                        phone="0534894260", zip_code="7522NB")
        customer_person_2.save()

    requirements = {}


@register_mock_gen
class OrganisationGen:
    model = Organisation

    @staticmethod
    def func():
        customer_person_1 = Person.objects.get(address="Drienerlolaan 5", city="Enschede", email="bestuur@iapc.utwente.nl",
                                        name="Jaap de Steen", phone="0534893927", zip_code="7522NB")

        organisation = Organisation(
                                        address="Drienerlolaan 5", city="Enschede",
                                        email="schaduwbestuur@iapc.utwente.nl", name="Shitty Company Ltd",
                                        phone="0534894260", zip_code="7522NB")
        organisation.save()
        customer_contact_organisation = ContactOrganisation(contact=customer_person_1,
                                                                 organisation=organisation)
        customer_contact_organisation.save()

    requirements = {Person}


@register_mock_gen
class ContactOrganisationGen:
    model = ContactOrganisation

    @staticmethod
    def func():
        customer_person_1 = Person.objects.get(address="Drienerlolaan 5", city="Enschede", email="bestuur@iapc.utwente.nl",
                                               name="Jaap de Steen", phone="0534893927", zip_code="7522NB")
        customer_person_2 = Person.objects.get(address="Drienerlolaan 5", city="Enschede",
                                        email="schaduwbestuur@iapc.utwente.nl", name="Gerda Steenhuizen",
                                        phone="0534894260", zip_code="7522NB")
        organisation = Organisation.objects.get(
            address="Drienerlolaan 5", city="Enschede",
            email="schaduwbestuur@iapc.utwente.nl", name="Shitty Company Ltd",
            phone="0534894260", zip_code="7522NB")
        organisation.save()
        customer_contact_organisation = ContactOrganisation(contact=customer_person_1,
                                                            organisation=organisation)
        customer_contact_organisation.save()
        customer_contact_organisation = ContactOrganisation(contact=customer_person_2,
                                                            organisation=organisation)
        customer_contact_organisation.save()

    requirements = {}
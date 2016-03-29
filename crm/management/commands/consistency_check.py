from django.core.management.base import BaseCommand, CommandError

from crm.models import Organisation, Person, ContactOrganisation, Customer


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Starting consistency check for the CRM module.")

        # Define results storage. This is a list of dicts, wherein the dicts have the following structure:
        # {'model': 'TheModel', 'reason', 'The reason', 'object': ModelInstance}
        inconsistencies = []  # type: list(dict(str,str))

        # Check organisations.
        organisations = [o.verify() for o in Organisation.objects.all()]  # type: list(tuple(bool,str,Organisation))

        # If not all verifications were OK, add the not-OK ones to the inconsistencies
        if not all([res[0] for res in organisations]):
            for result in [r for r in organisations if not r[0]]:
                inconsistencies.append({'model': 'Organisation', 'reason': result[1], 'object': result[2]})

        # Check Persons
        persons = [p.verify() for p in Person.objects.all()]  # type: list(tuple(bool,str,Person))

        # If not all verifications were OK, add the not-OK ones to the inconsistencies
        if not all([res[0] for res in persons]):
            for result in [r for r in persons if not r[0]]:
                inconsistencies.append({'model': 'Person', 'reason': result[1], 'object': result[2]})

        # Check ContactOrganisation
        contact_organisations = [co.verify() for co in
                                 ContactOrganisation.objects.all()]  # type: list(tuple(bool,str,ContactOrganisation))

        # If not all verifications were OK, add the not-OK ones to the inconsistencies
        if not all([res[0] for res in contact_organisations]):
            for result in [r for r in contact_organisations if not r[0]]:
                inconsistencies.append({'model': 'ContactOrganisation', 'reason': result[1], 'object': result[2]})

        # Check Customers
        customers = [p.verify() for p in Customer.objects.all()]  # type: list(tuple(bool,str,Customer))

        # If not all verifications were OK, add the not-OK ones to the inconsistencies
        if not all([res[0] for res in customers]):
            for result in [r for r in customers if not r[0]]:
                inconsistencies.append({'model': 'Customer', 'reason': result[1], 'object': result[2]})

        print("Finished consistency check for the CRM module.")
        if len(inconsistencies) != 0:
            print("Found inconsistencies:")
            for i in inconsistencies:
                print("  Model {}, instance {}: {}".format(i['model'],
                                                           "Unknown" if i['object'] is None else i['object'].pk,
                                                           i['reason']))
        else:
            print("No inconsistencies found.")
